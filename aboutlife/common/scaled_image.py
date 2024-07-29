# thanks https://discourse.gnome.org/t/how-to-auto-resize-images-according-to-window-size/7494

import cairo
import gi
from enum import Enum

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


class ScaledImageWidget(Gtk.DrawingArea):
    class STYLE(Enum):
        SCALED = 0  # the image is always fully visible
        ZOOMED = 1  # fill all available space
        FILL_H = 2  # image is scaled to fill horizontally
        FILL_V = 3  # image is scaled to fill vertically

    def __init__(self, style: STYLE = STYLE.SCALED):
        super().__init__()
        self.surface = None
        self.style = style
        self.connect("draw", self.on_draw)

    def set_image(self, image_path):
        # Load the image with GdkPixbuf
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)

        # Create a cairo ImageSurface from the pixbuf
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, pixbuf.get_width(), pixbuf.get_height()
        )
        cr = cairo.Context(self.surface)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()

        self.queue_draw()

    def on_draw(self, widget, cr):
        if not self.surface:
            return

        allocation = self.get_allocation()
        widget_width = allocation.width
        widget_height = allocation.height

        img_width = self.surface.get_width()
        img_height = self.surface.get_height()

        scale_x = widget_width / img_width
        scale_y = widget_height / img_height
        scale_factor = scale_x  # FILL_H

        if self.style == self.STYLE.SCALED:
            scale_factor = min(scale_x, scale_y)
        elif self.style == self.STYLE.ZOOMED:
            scale_factor = max(scale_x, scale_y)
        elif self.style == self.STYLE.FILL_V:
            scale_factor = scale_y

        # center the image within the widget
        translate_x = (widget_width - scale_factor * img_width) / 2
        translate_y = (widget_height - scale_factor * img_height) / 2

        cr.translate(translate_x, translate_y)
        cr.scale(scale_factor, scale_factor)
        cr.set_source_surface(self.surface, 0, 0)
        cr.paint()
