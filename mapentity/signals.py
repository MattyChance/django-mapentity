from __future__ import unicode_literals

from django import dispatch

post_register = dispatch.Signal(providing_args=["app_label", "model"])
