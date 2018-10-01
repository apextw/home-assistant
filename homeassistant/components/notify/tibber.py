"""
Pushbullet platform for notify component.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/notify.tibber/
"""
import asyncio
import logging

from homeassistant.components.notify import (
    ATTR_TITLE, ATTR_TITLE_DEFAULT, BaseNotificationService)
from homeassistant.components.tibber import DOMAIN


_LOGGER = logging.getLogger(__name__)


def get_service(hass, config, discovery_info=None):
    """Get the Pushbullet notification service."""
    tibber_connection = hass.data[DOMAIN]
    return TibberNotificationService(tibber_connection.send_notification)


class TibberNotificationService(BaseNotificationService):
    """Implement the notification service for Tibber."""

    def __init__(self, notify):
        """Initialize the service."""
        self._notify = notify

    async def async_send_message(self, message=None, **kwargs):
        """Send a message to Tibber devices."""
        title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
        try:
            await self._notify(title=title, message=message)
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout sending message with Tibber.")
