"""Hooks that are executed during and after install.
"""
import os
import frappe

def after_install():
    set_app_name()
    disable_signup()

def set_app_name():
    app_name = os.getenv("FRAPPE_APP_NAME")
    if app_name:
        frappe.db.set_value('System Settings', None, 'app_name', app_name)

def disable_signup():
    frappe.db.set_value("Website Settings", None, "disable_signup", 1)
