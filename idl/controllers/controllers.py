# -*- coding: utf-8 -*-

import json
import logging
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
    # def checkout_redirection(self, order):
    #     # must have a draft sales order with lines at this point, otherwise reset
    #     if not order or order.state != "draft":
    #         request.session["sale_order_id"] = None
    #         request.session["sale_transaction_id"] = None
    #         return request.redirect("/shop")

    #     if order and not order.order_line:
    #         return request.redirect("/shop/cart")

    #     # if transaction pending / done: redirect to confirmation
    #     tx = request.env.context.get("website_sale_transaction")
    #     if tx and tx.state != "draft":
    #         return request.redirect("/shop/payment/confirmation/%s" % order.id)

    @http.route(
        ["/shop/license_info"], type="http", auth="public", website=True, sitemap=False
    )
    def license_info(self, **post):

        # check that cart is valid
        # order = request.website.sale_get_order()
        # order = request.website.sale_get_order()
        # redirection = self.checkout_redirection(order)
        # if redirection:
        #     return redirection
        values = {}
        if post.get("sale_order_id") is None:
            pass
        else:
            order = request.website.env["sale.order"].search(
                [("id", "=", int(request.session["sale_order_id"]))]
            )[0]
            if len(order.order_line) == 1:
                values.update(
                    {
                        "fname": order.order_line[0].fname,
                    }
                )
        product = request.website.env["product.template"].search(
            [("name", "=", "UIDD")]
        )[0]
        # order._cart_update(
        #     product_id=int(product),
        #     add_qty=1,
        #     set_qty=1,
        #     # product_custom_attribute_values=product_custom_attribute_values,
        #     # no_variant_attribute_values=no_variant_attribute_values
        # )
        values.update(
            {
                # "search": search,
                # "category": category,
                # "pricelist": pricelist,
                # "attrib_values": attrib_values,
                # "attrib_set": attrib_set,
                # "keep": keep,
                # "categories": categs,
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

        sale_order._cart_update(
            product_id=1,
            set_qty=1,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
        )
        sale_order.order_line.write(
            {
                "fname": kw.get("fname"),
                "lname": kw.get("lname"),
                "city": kw.get("city"),
                "state_province": kw.get("state_province"),
                "zip_pc": kw.get("zip_pc"),
                "country_id": kw.get("country_id"),
                "birth": kw.get("birth"),
                "your_photo": kw.get("your_photo"),
                "country_birth": kw.get("country_birth"),
                # "category": kw.get("category"),
                "license_n": kw.get("license_n"),
                "license_d": kw.get("license_d"),
                "license_s": kw.get("license_s"),
                "license_p": kw.get("license_p"),
            }
        )
        # if kw.get("express"):
        return request.redirect("/shop/checkout?express=1")

        # return request.redirect("/shop/cart")
        return self.license_info()
