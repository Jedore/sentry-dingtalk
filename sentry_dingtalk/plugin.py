"""
  @Project     : sentry-dingtalk
  @Time        : 2021/07/12 17:34:35
  @File        : plugin.py
  @Author      : Jedore
  @Software    : VSCode
  @Desc        : 
"""


import requests
import six
from sentry import tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_plugins.base import CorePluginMixin
from django.conf import settings


class DingTalkPlugin(CorePluginMixin, notify.NotificationPlugin):
    title = "DingTalk"
    slug = "dingtalk"
    description = "Post notifications to Dingtalk."
    conf_key = "dingtalk"
    required_field = "webhook"
    author = "Jedore"
    author_url = "https://github.com/Jedore/sentry-dingtalk"
    version = "1.0.3"
    resource_links = [
        ("Report Issue", "https://github.com/Jedore/sentry-dingtalk/issues"),
        ("View Source", "https://github.com/Jedore/sentry-dingtalk"),
    ]

    feature_descriptions = [
        FeatureDescription(
            """
                Configure rule based Dingtalk notifications to automatically be posted into a
                specific channel.
                """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "Webhook URL",
                "type": "url",
                "placeholder": "https://oapi.dingtalk.com/robot/send?access_token=**********",
                "required": True,
                "help": "Your custom dingding webhook URL.",
                "default": self.set_default(project, "webhook", "DINGTALK_WEBHOOK"),
            },
            {
                "name": "custom_keyword",
                "label": "Custom Keyword",
                "type": "string",
                "placeholder": "e.g. [Sentry] Error title",
                "required": False,
                "help": "Optional - A custom keyword as the prefix of the event title",
                "default": self.set_default(
                    project, "custom_keyword", "DINGTALK_CUSTOM_KEYWORD"
                ),
            },
            {
                "name": "signature",
                "label": "Additional Signature",
                "type": "string",
                "required": False,
                "help": "Optional - Attach Dingtalk webhook signature to the request headers.",
                "default": self.set_default(project, "signature", "DINGTALK_SIGNATURE"),
            },
        ]

    def set_default(self, project, option, env_var):
        if self.get_option(option, project) != None:
            return self.get_option(option, project)
        if hasattr(settings, env_var):
            return six.text_type(getattr(settings, env_var))
        return None

    def notify(self, notification, raise_exception=False):
        event = notification.event
        group = event.group
        project = group.project
        self._post(group, project)

    def notify_about_activity(self, activity):
        project = activity.project
        group = activity.group
        self._post(group, project)

    def _post(self, group, project):
        webhook = self.get_option("webhook", project)
        custom_keyword = self.get_option("custom_keyword", project)
        signature = self.get_option("signature", project)

        issue_link = group.get_absolute_url(params={"referrer": "dingtalk"})

        payload = f"## {custom_keyword}\n\n" if custom_keyword else ""
        payload = f"{payload} #### Project: {project.name} \n\n"
        payload = f"{payload} ### Error: [{group.title}]({issue_link}) \n\n"
        payload = f"{payload} #### Detail: {group.message} \n\n"

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "charset": "utf8"
        }

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": group.title,
                "text": payload,
            },
        }

        requests.post(webhook, data=json.dumps(data), headers=headers)
