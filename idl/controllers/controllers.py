# -*- coding: utf-8 -*-

import json
import logging

import base64
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.fields import Command
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.osv import expression
from odoo.tools.json import scriptsafe as json_scriptsafe

_logger = logging.getLogger(__name__)


class WebsiteSale(http.Controller):
    @http.route(
        ["/shop/license_info"], type="http", auth="public", website=True, sitemap=False
    )
    def license_info(self, **post):

        values = {}
        order = request.website.sale_get_order()
        print(order.id)
        print(order.order_line)
        if order is False:
            pass
        else:
            if len(order.order_line):
                values.update(
                    {
                        "fname": order.order_line[0].fname,
                        "lname": order.order_line[0].lname,
                        "city": order.order_line[0].city,
                        "state_province": order.order_line[0].state_province,
                        "zip_pc": order.order_line[0].zip_pc,
                        "country_id": order.order_line[0].country_id,
                        "birth": order.order_line[0].birth,
                        "your_photo": order.order_line[0].your_photo,
                        "country_birth": order.order_line[0].country_birth,
                        # "category": order.order_line[0].category"),
                        "license_n": order.order_line[0].license_n,
                        "license_d": order.order_line[0].license_d,
                        "license_s": order.order_line[0].license_s,
                        "license_p": order.order_line[0].license_p,
                    }
                )
        product = request.website.env["product.template"].search(
            [("name", "=", "UIDD")]
        )[0]
        values.update(
            {
                "main_object": product,
                "product": product,
                "add_qty": 1,
                # "view_track": view_track,
                # "product": order,
                "post": post,
                "escape": lambda x: x.replace("'", r"\'"),
                # "partner": order.partner_id.id,
                # "order": order,
                "country_id": request.website.env["res.country"].search([]),
            }
        )
        print("asdads" * 88)
        print(post)
        print(values)
        return request.render("idl.license_info", values)

    @http.route(
        ["/shop/get_order"], type="http", auth="public", website=True, sitemap=False
    )
    def get_license_order(self, **kw):
        print(" get " * 88)
        print(kw)
        """This route is called when adding a product to cart."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != "draft":
            request.session["sale_order_id"] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get("product_custom_attribute_values"):
            product_custom_attribute_values = json_scriptsafe.loads(
                kw.get("product_custom_attribute_values")
            )

        no_variant_attribute_values = None
        if kw.get("no_variant_attribute_values"):
            no_variant_attribute_values = json_scriptsafe.loads(
                kw.get("no_variant_attribute_values")
            )
        product = request.website.env["product.template"].search(
            [("name", "=", "UIDD")]
        )[0]
        sale_order._cart_update(
            product_id=product.id,
            set_qty=1,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
        )
        # for ffields in ["your_photo", "license_s", "license_p"]:
        #     if kw.get(ffields):
        #         FileStorage = kw.get(ffields)
        #         FileExtension = FileStorage.filename.split(".")[-1].lower()
        #         ALLOWED_IMAGE_EXTENSIONS = ["jpg", "png", "gif"]
        #     if FileExtension not in ALLOWED_IMAGE_EXTENSIONS:
        #         return json.dumps(
        #             {
        #                 "status": 400,
        #                 "message": _(
        #                     "Only allowed image file with extension: %s"
        #                     % (",".join(ALLOWED_IMAGE_EXTENSIONS))
        #                 ),
        #             }
        #         )

        #     FileData = FileStorage.read()
        #     file_base64 = base64.encodestring(FileData)
        # kw[fields] = file_base64
        sale_order.order_line.write(
            {
                "fname": kw.get("fname"),
                "lname": kw.get("lname"),
                "city": kw.get("city"),
                "state_province": kw.get("state_province"),
                "zip_pc": kw.get("zip_pc"),
                "country_id": kw.get("country_id"),
                "birth": kw.get("birth"),
                # "your_photo": kw.get("your_photo"),
                "country_birth": kw.get("country_birth"),
                # "category": kw.get("category"),
                "license_n": kw.get("license_n"),
                "license_d": kw.get("license_d"),
                # "license_s": kw.get("license_s"),
                # "license_p": kw.get("license_p"),
            }
        )
        # if kw.get("express"):
        return request.redirect("/shop/checkout?express=1")

        # return request.redirect("/shop/cart")
        return self.license_info()
