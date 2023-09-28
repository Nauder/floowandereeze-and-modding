# === PROGRAM IMPORTS === #

import util as floo
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as TkFont
from os import remove
from os.path import join, isdir

from UnityPy import load as uload
from pygubu import Builder
from PIL import Image, ImageTk

from pathlib import Path
from shutil import copyfile
from math import gcd
from json import load, dump


# === APP ROOT DEFINITION === #


class Root:
    PROJECT_PATH = Path(__file__).parent
    PROJECT_UI = PROJECT_PATH / "Main.ui"
    MESSAGE = {
        "REPLACEMENT": "Asset Replacement",
        "EXTRACTION": "Asset Extraction",
        "SWAPPING": "Asset Swapping",
        "COPYING": "Bundle Copy",
    }
    FILE = {
        "IMAGE": ["*.png", "*.jpg", "*.jpeg"],
        "IMAGE_NAME": "image.png",
        "UNITY": "data.unity3d",
    }
    BUTTON = ["<Button-1>", "<Button-3>"]

    def __init__(self, master=None):
        # === APP STARTUP === #

        self.data = load(open("data.json", "r+"))
        self.field_flip_index = 9  # Needed as some fields have different orientation
        self.sleeve_to_replace = -1
        self.sleeve_dx_to_replace = -1
        self.sleeve_dx_part = -1
        self.field_to_replace = -1
        self.graves_to_replace = [-1, -1]
        self.bases_to_replace = [-1, -1]
        self.fields_to_replace = [-1, -1]
        self.mates_to_replace = [-1, -1]
        self.icon_to_replace = -1
        self.sleeves_img = []
        self.sleeves_dx_img = []
        self.fields_img = []
        self.graves_img = []
        self.bases_img = []
        self.full_fields_img = []
        self.icons_img = []
        self.mates_img = []
        self.home_bg_img = []
        self.first_list = [self.data["icons"][a][0] for a in self.data["icons"]]
        self.builder = builder = Builder()
        builder.add_resource_path(self.PROJECT_PATH)
        builder.add_from_file(self.PROJECT_UI)

        # === UI OBJECTS DEFINITION === #

        self.mainwindow = builder.get_object("toplevel1", master)
        self.card = builder.get_object("card")
        self.check_sleeve = builder.get_object("checkSleeve")
        self.card_dx = builder.get_object("cardDx")
        self.check_sleeve_dx = builder.get_object("checkSleeveDx")
        self.field = builder.get_object("field")
        self.icon = builder.get_object("icon")
        self.field_path = builder.get_object("fieldPath")
        self.filter_field = builder.get_object("filterField")
        self.image_path = builder.get_object("imagePath")
        self.sleeve_dx_path = builder.get_object("sleeveDxPath")
        self.game_path = builder.get_object("gamePath")
        self.blocker = builder.get_object("blocker")
        self.blocker_art = builder.get_object("blockerArt")
        self.sleeves = builder.get_object("sleeves")
        self.sleeves_dx = builder.get_object("sleevesDx")
        self.fields = builder.get_object("fields")
        self.graves = builder.get_object("graves")
        self.graves_lbl = [builder.get_object("grave1"), builder.get_object("grave2")]
        self.bases = builder.get_object("bases")
        self.bases_lbl = [builder.get_object("base1"), builder.get_object("base2")]
        self.full_fields = builder.get_object("full_fields")
        self.full_fields_lbl = [
            builder.get_object("full_field1"),
            builder.get_object("full_field2"),
        ]
        self.mates = builder.get_object("mates")
        self.mates_lbl = [builder.get_object("mate1"), builder.get_object("mate2")]
        self.icons = builder.get_object("icons")
        self.art_box = builder.get_object("cbName")
        self.art_path = builder.get_object("cardPath")
        self.card_art = builder.get_object("cardArt")
        self.wallpaper_box = builder.get_object("cbWP")
        self.wallpaper_path = [builder.get_object("wppPath")]
        self.wallpaper_art = builder.get_object("wallpaper")
        self.wallpaper_ratio = builder.get_object("ratio")
        self.icon_path = builder.get_object("iconPath")
        self.home_path = builder.get_object("homePath")
        self.home_bg = builder.get_object("homeBg")
        self.card_box = builder.get_object("cbCard")
        self.face_path = builder.get_object("facePath")
        self.face = builder.get_object("face")
        self.bg = [builder.get_object("lbg" + str(i)) for i in range(1, 13)]

        self.sleeves.bind(
            self.BUTTON[0],
            lambda event: self.select_image(int(self.sleeves.index("current")[2:])),
        )
        self.sleeves.pack(expand=True, fill="both")
        self.sleeves_dx.bind(
            self.BUTTON[0],
            lambda event: self.select_sleeve_dx_image(
                int(self.sleeves_dx.index("current")[2:])
            ),
        )
        self.sleeves_dx.pack(expand=True, fill="both")
        self.fields.bind(
            self.BUTTON[0],
            lambda event: self.select_field_image(
                int(self.fields.index("current")[2:])
            ),
        )
        self.fields.pack(expand=True, fill="both")
        self.graves.bind(
            self.BUTTON[0],
            lambda event: self.select_grave_image(
                int(self.graves.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.graves.bind(
            self.BUTTON[1],
            lambda event: self.select_grave_image(
                int(self.graves.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.graves.pack(expand=True, fill="both")
        self.bases.bind(
            self.BUTTON[0],
            lambda event: self.select_base_image(
                int(self.bases.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.bases.bind(
            self.BUTTON[1],
            lambda event: self.select_base_image(
                int(self.bases.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.bases.pack(expand=True, fill="both")
        self.full_fields.bind(
            self.BUTTON[0],
            lambda event: self.select_full_field_image(
                int(self.full_fields.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.full_fields.bind(
            self.BUTTON[1],
            lambda event: self.select_full_field_image(
                int(self.full_fields.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.full_fields.pack(expand=True, fill="both")
        self.mates.bind(
            self.BUTTON[0],
            lambda event: self.select_mate_image(
                int(self.mates.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.mates.bind(
            self.BUTTON[1],
            lambda event: self.select_mate_image(
                int(self.mates.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.mates.pack(expand=True, fill="both")
        self.icons.bind(
            self.BUTTON[0],
            lambda event: self.select_icon_image(int(self.icons.index("current")[2:])),
        )
        self.icons.pack(expand=True, fill="both")
        self.art_box.bind(
            "<KeyRelease>",
            lambda event: self.art_values(
                [art for art, value in self.data["name"].items()]
            ),
        )

        self.__startup()
        self.__build_combo_boxes()
        self.__apply_cosmetics()
        self.__limit_filetypes()

        builder.connect_callbacks(self)

    # === EVENT METHODS === #

    def __limit_filetypes(self):
        self.image_path.config(filetypes=[("Image", self.FILE["IMAGE"])])
        self.art_path.config(filetypes=[("Image", self.FILE["IMAGE"])])
        self.field_path.config(filetypes=[("Image", self.FILE["IMAGE"])])
        self.wallpaper_path[0].config(filetypes=[("Image", self.FILE["IMAGE"])])
        # TODO add support for wallpaper background replacement
        self.icon_path.config(filetypes=[(".png Image", "*.png")])
        self.home_path.config(filetypes=[("Image", self.FILE["IMAGE"])])

    def __startup(self):
        if self.data["gamePath"] != "empty":
            self.game_path.config(path=self.data["gamePath"])
            self.fetch_thumbnails()
            self.blocker_art.place(x=1025, y=1025)

        self.image_path.config(path=self.data["lastImage"]) if self.data[
            "lastImage"
        ] != "empty" else None
        self.sleeve_dx_path.config(path=self.data["lastSleeveDx"]) if self.data[
            "lastSleeveDx"
        ] != "empty" else None
        self.art_path.config(path=self.data["lastArt"]) if self.data[
            "lastArt"
        ] != "empty" else None
        self.field_path.config(path=self.data["lastField"]) if self.data[
            "lastField"
        ] != "empty" else None
        self.icon_path.config(path=self.data["lastIcon"]) if self.data[
            "lastIcon"
        ] != "empty" else None
        self.home_path.config(path=self.data["lastHome"]) if self.data[
            "lastHome"
        ] != "empty" else None
        self.apply_background() if self.data["background"] != "empty" else None

    def __build_combo_boxes(self):
        self.wallpaper_box["values"] = [value for value in self.data["wallpaper_names"]]
        self.card_box["values"] = sorted(
            key for key, value in self.data["types"].items()
        )
        self.art_box["values"] = sorted(key for key, value in self.data["name"].items())

    def __apply_cosmetics(self):
        ttk.Style().configure("TNotebook", background="#0B1828")
        ttk.Style().map("TNotebook.Tab", foreground=[("selected", "#1B2838")])
        ttk.Style().configure("TNotebook.Tab", foreground="#0B1828")

        big_font = TkFont.Font(family="Helvetica", size=12)

        self.mainwindow.option_add("*TCombobox*Listbox*Font", big_font)
        self.mainwindow.option_add("*TCombobox*Listbox*Background", "#1B2838")
        self.mainwindow.option_add("*TCombobox*Listbox*Foreground", "#EEE")

        self.art_box.config(font=big_font)
        self.wallpaper_box.config(font=big_font)

    def replace_sleeve(self):
        if (
            self.game_path.cget("path") is not None
            and self.image_path.cget("path") is not None
            and self.sleeve_to_replace != -1
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastImage"] = self.image_path.cget("path")
            self.update_json()
            self.replace_bundle(
                self.data["adress"][self.sleeve_to_replace],
                "slv",
                self.check_sleeve.state(),
            )
            self.fetch_target_thumbnails([["sleeves", self.fetch_sleeve_thumb_list()]])
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Sleeve texture replaced successfully!"
            )

    def replace_sleeve_dx(self):
        if (
            self.game_path.cget("path") is not None
            and self.image_path.cget("path") is not None
            and self.sleeve_dx_to_replace != -1
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastSleeveDx"] = self.sleeve_dx_path.cget("path")
            self.update_json()
            self.replace_bundle(
                self.data["sleeveDeluxe"][self.sleeve_dx_to_replace],
                "slvDx",
                self.check_sleeve_dx.state(),
            )
            self.fetch_thumbnails()
            self.fetch_target_thumbnails(
                [["sleeves_dx", self.fetch_sleeve_dx_thumb_list()]]
            )
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Sleeve DX texture replaced successfully!"
            )

    def replace_art(self):
        if (
            self.game_path.cget("path") is not None
            and self.art_path.cget("path") is not None
            and self.art_box.get() is not None
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastArt"] = self.art_path.cget("path")
            self.update_json()
            self.replace_bundle(self.data["name"][self.art_box.get()], "crd")
            self.select_card_art()
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Card Art texture replaced successfully!"
            )

    def replace_field(self):
        if (
            self.game_path.cget("path") is not None
            and self.field_path.cget("path") is not None
            and self.field_to_replace != -1
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastField"] = self.field_path.cget("path")
            self.update_json()
            self.replace_bundle(
                self.data["field"][self.field_to_replace],
                "fld",
                self.filter_field.state(),
            )
            self.fetch_target_thumbnails([["fields", self.fetch_field_thumb_list()]])
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Field texture replaced successfully!"
            )

    def replace_icon(self):
        if (
            self.game_path.cget("path") is not None
            and self.icon_path.cget("path") is not None
            and self.icon_to_replace != -1
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastIcon"] = self.icon_path.cget("path")
            self.update_json()
            size = 0
            for sprite in self.fetch_sprite_list(self.icon_to_replace):
                self.replace_bundle(sprite, "ico", False, False, size)
                size += 1
            self.fetch_target_thumbnails([["icons", self.fetch_icon_thumb_list()]])
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Icon texture replaced successfully!"
            )

    def replace_wallpaper(self):
        if (
            self.game_path.cget("path") is not None
            and self.wallpaper_path[0] is not None
            and self.wallpaper_box.current() is not None
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastWallpaper"][0] = self.wallpaper_path[0].cget("path")
            # self.data["lastWallpaper"][1] = self.wallpaperPath[1].cget('path')
            self.update_json()
            size = 0
            for part in self.data["wallpaper"][self.wallpaper_box.current()]:
                self.replace_bundle(part, "wpp", False, False, size)
                size += 1
            self.select_wallpaper_art()
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Wallpaper texture replaced successfully!"
            )

    def replace_home_bg(self):
        if (
            self.game_path.cget("path") is not None
            and self.home_path.cget("path") is not None
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastHome"] = self.home_path.cget("path")
            self.update_json()
            self.replace_unity3d_asset(
                "ShopBGBase02",
                floo.convert_image(self.home_path.cget("path"), (1920, 1080)),
            )
            self.fetch_thumbnails()
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Home BG texture replaced successfully!"
            )

    def replace_face(self):
        if (
            self.game_path.cget("path") is not None
            and self.face_path.cget("path") is not None
        ):
            self.data["gamePath"] = self.game_path.cget("path")
            self.data["lastFace"] = self.face_path.cget("path")
            self.update_json()
            self.replace_unity3d_asset(
                self.data["types"][self.card_box.get()],
                floo.convert_image(self.face_path.cget("path"), (704, 1024)),
                True,
            )
            self.select_face()
            floo.show_message(
                self.MESSAGE["REPLACEMENT"], "Card face texture replaced successfully!"
            )

    def setup_sleeves(self, d):
        self.data["gamePath"] = self.game_path.cget("path")
        self.fetch_thumbnails()
        self.blocker_art.place(x=1025, y=1025)

    def extract_sleeve(self):
        if (
            self.game_path.cget("path") is not None
            and self.image_path.cget("path") is not None
            and self.sleeve_to_replace != -1
        ):
            self.extract_texture(
                self.data["adress"][self.sleeve_to_replace],
                self.data["adress"][self.sleeve_to_replace],
            )
            floo.show_message(
                self.MESSAGE["EXTRACTION"],
                'Sleeve image exported to the "images" folder!',
            )

    def extract_sleeve_dx(self):
        if self.game_path.cget("path") is not None and self.sleeve_dx_to_replace != -1:
            self.extract_texture(
                self.data["sleeveDeluxe"][self.sleeve_dx_to_replace],
                self.data["sleeveDeluxe"][self.sleeve_dx_to_replace] + "_1",
            )
            self.extract_texture(
                self.data["sleeveDeluxe"][self.sleeve_dx_to_replace],
                self.data["sleeveDeluxe"][self.sleeve_dx_to_replace] + "_2",
            )
            floo.show_message(
                self.MESSAGE["EXTRACTION"],
                'Sleeve images exported to the "images" folder!',
            )

    def extract_art(self):
        if (
            self.game_path.cget("path") is not None
            and self.art_path.cget("path") is not None
            and self.art_box.get() is not None
        ):
            self.extract_texture(
                self.data["name"][self.art_box.get()], self.art_box.get()
            )
            floo.show_message(
                self.MESSAGE["EXTRACTION"], 'Card art exported to the "images" folder!'
            )

    def extract_field(self):
        if self.game_path.cget("path") is not None and self.field_to_replace != -1:
            self.extract_texture(
                self.data["field"][self.field_to_replace],
                self.data["field"][self.field_to_replace],
            )
            floo.show_message(
                self.MESSAGE["EXTRACTION"],
                'Field texture exported to the "images" folder!',
            )

    def extract_icon(self):
        if self.game_path.cget("path") is not None and self.icon_to_replace != -1:
            self.extract_texture(
                self.first_list[self.icon_to_replace],
                self.first_list[self.icon_to_replace],
            )
            floo.show_message(
                self.MESSAGE["EXTRACTION"],
                'Icon image exported to the "images" folder!',
            )

    def extract_wallpaper(self):
        if (
            self.game_path.cget("path") is not None
            and self.wallpaper_box.current() is not None
        ):
            for wallpaper_part in self.data["wallpaper"][self.wallpaper_box.current()]:
                self.extract_texture(wallpaper_part, wallpaper_part)
            floo.show_message(
                self.MESSAGE["EXTRACTION"],
                'Monster art exported to the "images" folder!',
            )

    def extract_home_bg(self):
        if self.game_path.cget("path") is not None:
            self.extract_unity3d_image("ShopBGBase02")
            floo.show_message(
                self.MESSAGE["EXTRACTION"], 'Home BG exported to the "images" folder!'
            )

    def extract_face(self):
        if (
            self.game_path.cget("path") is not None
            and self.card_box.current() is not None
        ):
            self.extract_unity3d_image(self.data["types"][self.card_box.get()], True)
            floo.show_message(
                self.MESSAGE["EXTRACTION"], 'Card face exported to the "images" folder!'
            )

    def swap_graves(self):
        if self.game_path.cget("path") is not None and -1 not in self.graves_to_replace:
            self.data["gamePath"] = self.game_path.cget("path")
            self.swap_bundles(
                [
                    self.data["grave"][0][self.graves_to_replace[0]],
                    self.data["grave"][0][self.graves_to_replace[1]],
                ]
            )
            self.swap_bundles(
                [
                    self.data["grave"][1][self.graves_to_replace[0]],
                    self.data["grave"][1][self.graves_to_replace[1]],
                ]
            )
            self.update_json()
            floo.show_message(
                self.MESSAGE["SWAPPING"], "Grave meshes swapped successfully!"
            )
            self.fetch_target_thumbnails([["graves", self.fetch_swap_list("grave")]])

    def swap_bases(self):
        if self.game_path.cget("path") is not None and -1 not in self.bases_to_replace:
            self.data["gamePath"] = self.game_path.cget("path")
            self.swap_bundles(
                [
                    self.data["base"][0][self.bases_to_replace[0]],
                    self.data["base"][0][self.bases_to_replace[1]],
                ]
            )
            self.swap_bundles(
                [
                    self.data["base"][1][self.bases_to_replace[0]],
                    self.data["base"][1][self.bases_to_replace[1]],
                ]
            )
            self.update_json()
            floo.show_message(
                self.MESSAGE["SWAPPING"], "Mate base meshes swapped successfully!"
            )
            self.fetch_target_thumbnails([["bases", self.fetch_swap_list("base")]])

    def swap_fields(self):
        if self.game_path.cget("path") is not None and -1 not in self.fields_to_replace:
            self.data["gamePath"] = self.game_path.cget("path")
            self.swap_bundles(
                [
                    self.data["full_field"][0][self.fields_to_replace[0]],
                    self.data["full_field"][0][self.fields_to_replace[1]],
                ]
            )
            self.swap_bundles(
                [
                    self.data["full_field"][1][self.fields_to_replace[0]],
                    self.data["full_field"][1][self.fields_to_replace[1]],
                ]
            )
            self.update_json()
            floo.show_message(
                self.MESSAGE["SWAPPING"], "Field meshes swapped successfully!"
            )
            self.fetch_target_thumbnails(
                [
                    ["full_fields", self.fetch_swap_list("full_field")],
                    ["fields", self.fetch_field_thumb_list()],
                ]
            )

    def swap_mates(self):
        if self.game_path.cget("path") is not None and -1 not in self.mates_to_replace:
            self.data["gamePath"] = self.game_path.cget("path")
            self.swap_bundles(
                [
                    self.data["mate"][0][self.mates_to_replace[0]],
                    self.data["mate"][0][self.mates_to_replace[1]],
                ]
            )
            self.swap_bundles(
                [
                    self.data["mate"][1][self.mates_to_replace[0]],
                    self.data["mate"][1][self.mates_to_replace[1]],
                ]
            )
            self.update_json()
            floo.show_message(
                self.MESSAGE["SWAPPING"], "Mate meshes swapped successfully!"
            )
            self.fetch_target_thumbnails([["mates", self.fetch_swap_list("mate")]])

    def copy_bundle(self, source_id) -> None:
        bundles = []

        match source_id:
            case "card_art":
                bundles = [self.data["name"][self.art_box.get()]]
            case "sleeve":
                bundles = [self.data["adress"][self.sleeve_to_replace]]
            case "sleeve_dx":
                bundles = [self.data["sleeveDeluxe"][self.sleeve_dx_to_replace]]
            case "mat":
                bundles = [self.data["field"][self.field_to_replace]]
            case "player_icon":
                bundles = self.data["icons"][
                    list(self.data["icons"].keys())[self.icon_to_replace]
                ]
            case "home_art":
                bundles = self.data["wallpaper"][self.wallpaper_box.current()]

        for bundle in bundles:
            copyfile(
                join(self.data["gamePath"], "0000", bundle[:2], bundle),
                join("bundles", source_id, bundle),
            )

        floo.show_message(
            self.MESSAGE["COPYING"],
            f'Bundle(s) copied to the "bundles/{source_id}" folder!',
        )

    def get_card_art(self, d):
        self.select_card_art()

    def get_wallpaper_art(self, d):
        self.select_wallpaper_art()

    def get_face(self, d):
        self.select_face()

    def set_background(self):
        if (
            self.game_path.cget("path") is not None
            and self.art_path.cget("path") is not None
        ):
            self.data["background"] = self.art_path.cget("path")
            self.update_json()
            self.apply_background()
            floo.show_message("Background", "App background set!")

    def reset_background(self):
        if self.game_path.cget("path") is not None:
            self.data["background"] = "empty"
            self.update_json()
            floo.show_message("Background", "App background will reset on restart!")

    def run(self):
        self.mainwindow.mainloop()

    # === UNITY RELATED METHODS === #

    def fetch_image(
        self, bundle: str, aspect: str, miss=False, simple_aspect=(0, 0)
    ) -> Image.Image:
        """Fetches an image from a Bundle, applying its proper aspect ratio"""

        env = uload(self.prepare_environment(miss, bundle))

        for obj in env.objects:
            found = False
            if obj.type.name == "Texture2D":
                data = obj.read()

                if aspect == "smp":
                    img = data.image.resize(simple_aspect, Image.Resampling.LANCZOS)
                    found = True
                elif aspect == "slvDx_1":
                    if "_1" in data.name:
                        img = data.image.resize((512, 746))
                        found = True
                elif aspect == "slvDx_2":
                    if "_2" in data.name:
                        img = data.image.resize((512, 746))
                        found = True
                elif aspect == "wpp":
                    img = data.image
                    img.thumbnail((760, 760), Image.Resampling.LANCZOS)
                    found = True
                elif aspect == "fld":
                    if "01_BaseColor_near" in data.name:
                        img = data.image
                        if self.field_to_replace < self.field_flip_index:
                            img_field = img.crop((0, 311, 2048, 1023)).rotate(180)
                        else:
                            img_field = img.crop((0, 243, 2048, 955))
                        img_field.thumbnail(
                            (900, img_field.size[1]), Image.Resampling.LANCZOS
                        )
                        img = img_field
                        found = True
                else:
                    img = data.image
                    found = True

                if found:
                    img.convert("RGB")
                    img.name = "image.jpg"
                    return img

        return self.fetch_image(bundle, aspect, True, simple_aspect)

    def fetch_unity3d_image(self, path_id: str, aspect: tuple) -> Image.Image:
        """Fetches an image from the unity3d file, applying its proper aspect ratio"""

        env = uload(
            join(self.data["gamePath"][:-18], "masterduel_Data", self.FILE["UNITY"])
        )

        for obj in env.objects:
            if obj.type.name == "Texture2D" and str(obj.path_id) == path_id:
                data = obj.read()
                img = data.image.resize(aspect)
                img.convert("RGB")
                img.name = "image.jpg"
                return img

    def fetch_sleeve_thumb_list(self) -> list[ImageTk.PhotoImage]:
        """Fetches the sleeve thumbnail list used by the app"""

        images_list = []
        for i in self.data["adress"]:
            f_path = join(self.data["gamePath"], "0000", i[:2], i)
            env = uload(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    img = data.image.resize((128, 181))
                    img.convert("RGB")
                    img.name = self.FILE["IMAGE_NAME"]
                    sleeve = ImageTk.PhotoImage(img)
                    images_list.append(sleeve)

        return images_list

    def fetch_sleeve_dx_thumb_list(self) -> list[ImageTk.PhotoImage]:
        """Fetches the deluxe sleeve thumbnail list used by the app"""

        images_list = []
        for i in self.data["sleeveDeluxe"]:
            f_path = join(self.data["gamePath"], "0000", i[:2], i)
            env = uload(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    if "_1" in data.name or "_2" in data.name:
                        img = data.image.resize((187, 266))
                        img.convert("RGB")
                        img.name = self.FILE["IMAGE_NAME"]
                        sleeve = ImageTk.PhotoImage(img)
                        images_list.append(sleeve)

        return images_list

    def fetch_field_thumb_list(self) -> list[ImageTk.PhotoImage]:
        """Fetches the field thumbnail list used by the app"""

        images_list = []
        for i in self.data["field"]:
            f_path = join(self.data["gamePath"], "0000", i[:2], i)
            env = uload(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    if "01_BaseColor_near" in data.name:
                        img = data.image
                        img.convert("RGB")
                        img.name = self.FILE["IMAGE_NAME"]
                        img_field = (
                            img.crop((0, 311, 2048, 1023)).rotate(180)
                            if len(images_list) < self.field_flip_index
                            else img.crop((0, 243, 2048, 955))
                        )
                        img_field.thumbnail(
                            (662, img_field.size[1]), Image.Resampling.LANCZOS
                        )
                        field = ImageTk.PhotoImage(img_field)
                        images_list.append(field)

        return images_list

    def fetch_swap_list(self, part: str) -> list[ImageTk.PhotoImage]:
        """Fetches a swappable thumbnail list used by the app"""

        images_list = []
        for i in self.data[part][1]:
            f_path = join(self.data["gamePath"], "0000", i[:2], i)
            env = uload(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    img = data.image
                    img.convert("RGB")
                    img.thumbnail((141, 141), Image.Resampling.LANCZOS)
                    img.name = self.FILE["IMAGE_NAME"]
                    part_thumb = ImageTk.PhotoImage(img)
                    images_list.append(part_thumb)

        return images_list

    def fetch_icon_thumb_list(self) -> list[ImageTk.PhotoImage]:
        """Fetches the icon thumbnail list used by the app"""

        images_list = []

        for i in self.first_list:
            f_path = join(self.data["gamePath"], "0000", i[:2], i)
            env = uload(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    img = data.image.resize((129, 129))
                    img.convert("RGB")
                    img.name = self.FILE["IMAGE_NAME"]
                    icon = ImageTk.PhotoImage(img)
                    images_list.append(icon)

        return images_list

    def fetch_home_bg(self) -> ImageTk.PhotoImage:
        env = uload(
            join(self.data["gamePath"][:-18], "masterduel_Data", self.FILE["UNITY"])
        )
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if "ShopBGBase02" == data.name:
                    img = data.image.resize((1120, 630))
                    img.convert("RGB")
                    img.name = self.FILE["IMAGE_NAME"]
                    bg = ImageTk.PhotoImage(img)
                    return bg

    def fetch_thumbnails(self) -> None:
        """Fetches and creates the thumbnails used by the app"""

        if isdir(join(self.data["gamePath"], "0000", "00")):
            self.sleeves_img = self.fetch_sleeve_thumb_list()
            self.sleeves_dx_img = self.fetch_sleeve_dx_thumb_list()
            self.fields_img = self.fetch_field_thumb_list()
            self.graves_img = self.fetch_swap_list("grave")
            self.bases_img = self.fetch_swap_list("base")
            self.full_fields_img = self.fetch_swap_list("full_field")
            self.icons_img = self.fetch_icon_thumb_list()
            self.mates_img = self.fetch_swap_list("mate")
            self.home_bg_img = self.fetch_home_bg()

            ui_thumb_list = [
                [self.sleeves, self.sleeves_img],
                [self.sleeves_dx, self.sleeves_dx_img],
                [self.fields, self.fields_img],
                [self.graves, self.graves_img],
                [self.bases, self.bases_img],
                [self.full_fields, self.full_fields_img],
                [self.icons, self.icons_img],
                [self.mates, self.mates_img],
            ]

            for ui_object, thumb_list in ui_thumb_list:
                ui_object.config(state=tk.NORMAL)
                ui_object.delete("1.0", "end")

                for i in range(len(thumb_list)):
                    ui_object.image_create(tk.END, padx=2, pady=2, image=thumb_list[i])

                ui_object.config(state=tk.DISABLED)

            self.home_bg.configure(image=self.home_bg_img)
            self.home_bg.image = self.home_bg_img

            self.blocker.place(x=1025, y=1025)

        else:
            floo.show_error(
                "Invalid Game Path",
                "Application could not find the game assets in the given directory.",
            )

    def fetch_target_thumbnails(self, target: list) -> None:
        """Fetches and creates the thumbnails used by the given parts of the app"""

        for ui_object_reference, thumb_list in target:
            setattr(self, ui_object_reference + "_img", thumb_list)

            getattr(self, ui_object_reference).config(state=tk.NORMAL)
            getattr(self, ui_object_reference).delete("1.0", "end")

            for i in range(len(getattr(self, ui_object_reference + "_img"))):
                getattr(self, ui_object_reference).image_create(
                    tk.END,
                    padx=2,
                    pady=2,
                    image=getattr(self, ui_object_reference + "_img")[i],
                )

            getattr(self, ui_object_reference).config(state=tk.DISABLED)

    def fetch_sprite_list(self, indx: int) -> list:
        """Fetches the sprites bundles related to the user given index"""

        sprite_list = []
        count = 0

        for li in self.data["icons"]:
            if count == indx:
                sprite_list = self.data["icons"][li]
                sprite_list = self.sort_sprite_list(sprite_list)
                return sprite_list
            else:
                count += 1

        return sprite_list

    def swap_bundles(self, bundles: list) -> None:
        """Swaps the content of two given bundles"""

        asset_1 = join(self.data["gamePath"], "0000", bundles[0][:2], bundles[0])
        asset_2 = join(self.data["gamePath"], "0000", bundles[1][:2], bundles[1])

        copyfile(asset_1, join(self.data["gamePath"], bundles[0]))
        copyfile(asset_2, asset_1)
        copyfile(join(self.data["gamePath"], bundles[0]), asset_2)
        remove(join(self.data["gamePath"], bundles[0]))

    def replace_bundle(
        self, bundle: str, asset: str, filtered="empty", miss=False, size=-1
    ) -> None:
        """Replaces any image of the supported types inside a bundle with an image provided in the ui"""

        f_path = self.prepare_environment(miss, bundle)
        env = uload(f_path)

        found = False

        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()

                if asset == "slv":
                    img = (
                        floo.add_sleeve_border(
                            floo.convert_image(self.data["lastImage"], (480, 700))
                        )
                        if "selected" in filtered
                        else floo.convert_image(self.data["lastImage"], (480, 700))
                    )
                    found = True
                if asset == "slvDx":
                    if self.sleeve_dx_part == 0:
                        if "_2" in data.name:
                            img = (
                                floo.add_sleeve_border(
                                    floo.convert_image(
                                        self.data["lastSleeveDx"], (480, 700)
                                    )
                                )
                                if "selected" in filtered
                                else floo.convert_image(
                                    self.data["lastSleeveDx"], (480, 700)
                                )
                            )
                            found = True
                    else:
                        if "_1" in data.name:
                            img = (
                                floo.add_sleeve_border(
                                    floo.convert_image(
                                        self.data["lastSleeveDx"], (480, 700)
                                    )
                                )
                                if "selected" in filtered
                                else floo.convert_image(
                                    self.data["lastSleeveDx"], (480, 700)
                                )
                            )
                            found = True
                elif asset == "crd":
                    img = floo.convert_image(self.data["lastArt"], (512, 512))
                    found = True
                elif asset == "ico":
                    if size == 0:
                        s = 128
                    elif size == 1:
                        s = 256
                    elif size == 2:
                        s = 512
                    img = Image.open(self.data["lastIcon"]).resize((s, s))
                    found = True
                elif asset == "wpp":
                    if size == 0:
                        img = Image.open(self.data["lastWallpaper"][0])
                        wallpaper = data.image
                        img.thumbnail(
                            (wallpaper.width, wallpaper.height),
                            Image.Resampling.LANCZOS,
                        )
                        new_img = Image.new("RGBA", wallpaper.size)
                        new_img.paste(img)
                    else:
                        wallpaper = data.image
                        new_img = Image.new("RGBA", wallpaper.size)
                    img = new_img
                    found = True
                elif asset == "fld" and "01_BaseColor_near" in data.name:
                    img = data.image
                    if self.field_to_replace < self.field_flip_index:
                        mat = Image.open(self.data["lastField"]).rotate(180)
                    else:
                        mat = Image.open(self.data["lastField"])
                    while mat.size[0] < 2048 or mat.size[1] < 712:
                        mat = mat.resize((mat.size[0] * 2, mat.size[1] * 2))
                    mat.thumbnail((2048, mat.size[1]), Image.Resampling.LANCZOS)
                    mat_fit = mat.crop((0, 0, 2048, 712))
                    if self.field_to_replace < 6:
                        img.paste(mat_fit, (0, 311))
                    else:
                        img.paste(mat_fit, (0, 243))
                    if "selected" in filtered:
                        if self.field_to_replace < 6:
                            base = Image.open("res/base.png")
                        else:
                            base = Image.open("res/base_inv.png")
                        new_mat = Image.new("RGBA", img.size)
                        new_mat = Image.alpha_composite(new_mat, img)
                        new_mat = Image.alpha_composite(new_mat, base)
                        img = new_mat
                    found = True

                if found:
                    data.m_Width, data.m_Height = img.size
                    data.image = img

                    data.save()
                    break

            elif asset == "slv":
                type_tree = obj.read_typetree()
                if (
                    obj.type.name == "Material"
                    and "_LightPower"
                    in type_tree["m_SavedProperties"]["m_Floats"][10][0]
                ):
                    type_tree["m_SavedProperties"]["m_Floats"][10] = (
                        "_LightPower",
                        0.0,
                    )

                    obj.save_typetree(type_tree)
        else:
            self.replace_bundle(bundle, asset, filtered, True, size)
            return

        with open(f_path, "wb") as f:
            f.write(env.file.save())

    def replace_unity3d_asset(
        self, asset: str, img: Image.Image, by_path_id=False
    ) -> None:
        """Replaces a given asset contained within the unity3d self.file with an image provided in the self"""

        env = uload(
            join(self.data["gamePath"][:-18], "masterduel_Data", self.FILE["UNITY"])
        )
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if by_path_id and str(obj.path_id) == asset or asset == data.name:
                    data.m_Width, data.m_Height = img.size
                    data.image = img

                    data.save()

                    break

        with open(
            join(self.data["gamePath"][:-18], "masterduel_Data", "data.unity3d"), "wb"
        ) as f:
            f.write(env.file.save())

    def extract_texture(self, bundle: str, name: str, miss=False) -> None:
        """Extracts the given bundle's relevant image into the 'images' folder"""

        found = False

        for obj in uload(self.prepare_environment(miss, bundle)).objects:
            if obj.type.name == "Texture2D":
                data = obj.read()

                if name == self.data["field"][self.field_to_replace]:
                    if "01_BaseColor_near" in data.name:
                        found = True
                elif (
                    name == self.data["sleeveDeluxe"][self.sleeve_dx_to_replace] + "_1"
                ):
                    if "_1" in data.name:
                        found = True
                elif (
                    name == self.data["sleeveDeluxe"][self.sleeve_dx_to_replace] + "_2"
                ):
                    if "_2" in data.name:
                        found = True
                else:
                    found = True

                if found:
                    dest = join("Images", floo.slugify(name) + ".png")

                    img = data.image
                    img.save(dest)
                    break
        else:
            return self.extract_texture(bundle, name, True)

    def extract_unity3d_image(self, asset: str, by_id=False) -> None:
        """Extracts the relevant unity3d image into the 'images' folder"""

        for obj in uload(
            join(self.data["gamePath"][:-18], "masterduel_Data", self.FILE["UNITY"])
        ).objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if by_id:
                    if str(obj.path_id) == asset:
                        dest = join("Images", floo.slugify(data.name) + ".png")

                        img = data.image
                        img.save(dest)

                        break
                else:
                    if asset == data.name:
                        dest = join("Images", floo.slugify(data.name) + ".png")

                        img = data.image
                        img.save(dest)

                        break

    def select_image(self, indx: int) -> None:
        """Assigns the index of the image selected by the user to the global 'self.sleeve_to_replace' variable and
        applies it to the selected card image"""

        sleeve = ImageTk.PhotoImage(
            self.fetch_image(self.data["adress"][indx], "smp", False, (512, 746))
        )
        self.card.configure(image=sleeve)
        self.card.image = sleeve
        self.sleeve_to_replace = indx

    def select_sleeve_dx_image(self, indx: int) -> None:
        """Assigns the index of the image selected by the user to the global 'sleeve_dx_to_replace' variable and applies
        it to the selected card image"""

        self.sleeve_dx_to_replace = indx if indx % 2 == 0 else indx - 1
        self.sleeve_dx_part = indx % 2

        sleeve = ImageTk.PhotoImage(
            self.fetch_image(
                self.data["sleeveDeluxe"][self.sleeve_dx_to_replace],
                "slvDx_2" if indx % 2 == 0 else "slvDx_1",
            )
        )
        self.card_dx.configure(image=sleeve)
        self.card_dx.image = sleeve

    def select_field_image(self, indx: int) -> None:
        """Assigns the index of the image selected by the user to the global 'field_to_replace' variable and applies it
        to the selected field image"""

        self.field_to_replace = indx
        field = ImageTk.PhotoImage(self.fetch_image(self.data["field"][indx], "fld"))
        self.field.configure(image=field)
        self.field.image = field

    def select_grave_image(self, indx: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'graves_to_replace' variable and applies it
        to the selected grave image"""

        self.graves_to_replace[pair] = indx
        grave = ImageTk.PhotoImage(
            self.fetch_image(self.data["grave"][1][indx], "smp", False, (200, 200))
        )
        self.graves_lbl[pair].configure(image=grave)
        self.graves_lbl[pair].image = grave

    def select_base_image(self, indx: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'bases_to_replace' variable and applies it
        to the selected base image"""

        self.bases_to_replace[pair] = indx
        base = ImageTk.PhotoImage(
            self.fetch_image(self.data["base"][1][indx], "smp", False, (200, 200))
        )
        self.bases_lbl[pair].configure(image=base)
        self.bases_lbl[pair].image = base

    def select_full_field_image(self, indx: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'self.fields_to_replace' variable and
        applies it to the selected field image"""

        self.fields_to_replace[pair] = indx
        field = ImageTk.PhotoImage(
            self.fetch_image(self.data["full_field"][1][indx], "smp", False, (200, 200))
        )
        self.full_fields_lbl[pair].configure(image=field)
        self.full_fields_lbl[pair].image = field

    def select_mate_image(self, indx: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'bases_to_replace' variable and applies it
        to the selected base image"""

        self.mates_to_replace[pair] = indx
        mate = ImageTk.PhotoImage(
            self.fetch_image(self.data["mate"][1][indx], "smp", False, (200, 200))
        )
        self.mates_lbl[pair].configure(image=mate)
        self.mates_lbl[pair].image = mate

    def select_icon_image(self, indx: int) -> None:
        """Assigns the index of the image selected by the user to the global 'icon_to_replace' variable and applies it
        to the selected icon image"""

        self.icon_to_replace = indx
        icon = ImageTk.PhotoImage(
            self.fetch_image(self.first_list[indx], "smp", False, (200, 200))
        )
        self.icon.configure(image=icon)
        self.icon.image = icon

    def select_card_art(self) -> None:
        """Displays the card art of the card selected in the art combobox on-screen"""

        art = ImageTk.PhotoImage(
            self.fetch_image(
                self.data["name"][self.art_box.get()], "smp", False, (512, 512)
            )
        )
        self.card_art.configure(image=art)
        self.card_art.image = art

    def select_wallpaper_art(self) -> None:
        """Displays the art of the wallpaper selected in the wallpaper combobox on-screen, and it's art ratio"""

        art = ImageTk.PhotoImage(
            self.fetch_image(
                self.data["wallpaper"][self.wallpaper_box.current()][0], "wpp"
            )
        )
        self.wallpaper_art.configure(image=art)
        self.wallpaper_art.image = art
        self.wallpaper_ratio.configure(
            text=str(int(art.width() / gcd(art.width(), art.height())))
            + ":"
            + str(int(art.height() / gcd(art.width(), art.height())))
        )

    def select_face(self) -> None:
        """Displays the face of the card type selected in the face combobox on-screen"""

        face = ImageTk.PhotoImage(
            self.fetch_unity3d_image(
                self.data["types"][self.card_box.get()], (512, 746)
            )
        )
        self.face.configure(image=face)
        self.face.image = face

    def art_values(self, cache: list) -> None:
        """Filters the art combobox with the text inputted by the user"""

        i = self.art_box.get()
        db_list = [x for x in cache if i.upper() in x.upper()]
        self.art_box["values"] = sorted(db_list)

    def update_json(self) -> None:
        """Updates the data json with the session's data"""

        with open("data.json", "w") as f:
            dump(self.data, f)

    def sort_sprite_list(self, sprite_list: list) -> list:
        """Sorts a given sprite list by image size"""

        for sprite in sprite_list:
            sprite_art = self.fetch_image(sprite, "spt")

            if sprite_art.width == 128:
                small_sprite = sprite
            elif sprite_art.width == 256:
                medium_sprite = sprite
            elif sprite_art.width == 512:
                large_sprite = sprite

        return [small_sprite, medium_sprite, large_sprite]

    def prepare_environment(self, miss: bool, bundle: str) -> str:
        """returns the UnityPy environment path related to the bundle and game path given"""

        return (
            join(
                self.data["gamePath"][:-18],
                "masterduel_Data",
                "StreamingAssets",
                "AssetBundle",
                bundle[:2],
                bundle,
            )
            if miss
            else join(self.data["gamePath"], "0000", bundle[:2], bundle)
        )

    def apply_background(self):
        """Applies the art of the user selected card art as the app's background"""

        bg_img = Image.open(self.data["background"]).resize((1400, 800))
        bg_img.putalpha(64)
        bg_img = ImageTk.PhotoImage(bg_img)

        for screen in self.bg:
            screen.configure(image=bg_img)
            screen.image = bg_img


if __name__ == "__main__":
    Root().run()
