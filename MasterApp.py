# === PROGRAM IMPORTS === #

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as TkFont
from os.path import join, isdir

from pygubu import Builder
from PIL import Image, ImageTk

from shutil import copyfile
from math import gcd

from services.UnityService import UnityService
from util.constants import PROJECT_PATH, PROJECT_UI, DATA, BUTTON, FILE, MESSAGE
from util.data_utils import update_json
from util.image_utils import convert_image
from util.ui_utils import show_message, show_error
from util.unity_utils import replace_unity3d_asset, fetch_sleeve_thumb_list, fetch_unity3d_image, swap_bundles, \
    fetch_swap_list, fetch_home_bg, fetch_field_thumb_list, extract_unity3d_image


# === APP ROOT DEFINITION === #


class Root:
    def __init__(self, master=None):
        # === APP STARTUP === #

        self.service: UnityService = UnityService()
        self.sleeves_img: list[int] = []
        self.fields_img: list[int] = []
        self.graves_img: list[int] = []
        self.bases_img: list[int] = []
        self.full_fields_img: list[int] = []
        self.icons_img: list[int] = []
        self.mates_img: list[int] = []
        self.home_bg_img: list[int] = []
        self.builder = builder = Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # === UI OBJECTS DEFINITION === #

        self.mainwindow = builder.get_object("toplevel1", master)
        self.card = builder.get_object("card")
        self.check_sleeve = builder.get_object("checkSleeve")
        self.field = builder.get_object("field")
        self.icon = builder.get_object("icon")
        self.field_path = builder.get_object("fieldPath")
        self.filter_field = builder.get_object("filterField")
        self.image_path = builder.get_object("imagePath")
        self.game_path = builder.get_object("gamePath")
        self.blocker = builder.get_object("blocker")
        self.blocker_art = builder.get_object("blockerArt")
        self.sleeves = builder.get_object("sleeves")
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
        self.bg = [builder.get_object("lbg" + str(i)) for i in range(1, 12)]

        self.sleeves.bind(
            BUTTON[0],
            lambda event: self.select_image(int(self.sleeves.index("current")[2:])),
        )
        self.sleeves.pack(expand=True, fill="both")
        self.fields.bind(
            BUTTON[0],
            lambda event: self.select_field_image(
                int(self.fields.index("current")[2:])
            ),
        )
        self.fields.pack(expand=True, fill="both")
        self.graves.bind(
            BUTTON[0],
            lambda event: self.select_grave_image(
                int(self.graves.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.graves.bind(
            BUTTON[1],
            lambda event: self.select_grave_image(
                int(self.graves.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.graves.pack(expand=True, fill="both")
        self.bases.bind(
            BUTTON[0],
            lambda event: self.select_base_image(
                int(self.bases.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.bases.bind(
            BUTTON[1],
            lambda event: self.select_base_image(
                int(self.bases.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.bases.pack(expand=True, fill="both")
        self.full_fields.bind(
            BUTTON[0],
            lambda event: self.select_full_field_image(
                int(self.full_fields.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.full_fields.bind(
            BUTTON[1],
            lambda event: self.select_full_field_image(
                int(self.full_fields.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.full_fields.pack(expand=True, fill="both")
        self.mates.bind(
            BUTTON[0],
            lambda event: self.select_mate_image(
                int(self.mates.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.mates.bind(
            BUTTON[1],
            lambda event: self.select_mate_image(
                int(self.mates.index("current")[2:]), int(event.num / 2)
            ),
        )
        self.mates.pack(expand=True, fill="both")
        self.icons.bind(
            BUTTON[0],
            lambda event: self.select_icon_image(int(self.icons.index("current")[2:])),
        )
        self.icons.pack(expand=True, fill="both")
        self.art_box.bind(
            "<KeyRelease>",
            lambda event: self.art_values(
                [art for art, value in DATA["name"].items()]
            ),
        )

        self.__startup()
        self.__build_combo_boxes()
        self.__apply_cosmetics()
        self.__limit_filetypes()

        builder.connect_callbacks(self)

    # === EVENT METHODS === #

    def __limit_filetypes(self):
        self.image_path.config(filetypes=[("Image", FILE["IMAGE"])])
        self.art_path.config(filetypes=[("Image", FILE["IMAGE"])])
        self.field_path.config(filetypes=[("Image", FILE["IMAGE"])])
        self.wallpaper_path[0].config(filetypes=[("Image", FILE["IMAGE"])])
        self.icon_path.config(filetypes=[(".png Image", "*.png")])
        self.home_path.config(filetypes=[("Image", FILE["IMAGE"])])

    def __startup(self):
        if DATA["gamePath"] != "empty":
            self.game_path.config(path=DATA["gamePath"])
            self.fetch_thumbnails()
            self.blocker_art.place(x=1025, y=1025)

        self.image_path.config(path=DATA["lastImage"]) if DATA[
                                                              "lastImage"
                                                          ] != "empty" else None
        self.art_path.config(path=DATA["lastArt"]) if DATA[
                                                          "lastArt"
                                                      ] != "empty" else None
        self.field_path.config(path=DATA["lastField"]) if DATA[
                                                              "lastField"
                                                          ] != "empty" else None
        self.icon_path.config(path=DATA["lastIcon"]) if DATA[
                                                            "lastIcon"
                                                        ] != "empty" else None
        self.home_path.config(path=DATA["lastHome"]) if DATA[
                                                            "lastHome"
                                                        ] != "empty" else None
        self.apply_background() if DATA["background"] != "empty" else None

    def __build_combo_boxes(self):
        self.wallpaper_box["values"] = [value for value in DATA["wallpaper_names"]]
        self.card_box["values"] = sorted(
            key for key, value in DATA["types"].items()
        )
        self.art_box["values"] = sorted(key for key, value in DATA["name"].items())

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
                and self.service.sleeve_to_replace != -1
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastImage"] = self.image_path.cget("path")
            update_json()
            self.service.replace_bundle(
                DATA["adress"][self.service.sleeve_to_replace],
                "slv",
                self.check_sleeve.state(),
            )
            self.fetch_target_thumbnails([["sleeves", fetch_sleeve_thumb_list()]])
            show_message(
                MESSAGE["REPLACEMENT"], "Sleeve texture replaced successfully!"
            )

    def replace_art(self):
        if (
                self.game_path.cget("path") is not None
                and self.art_path.cget("path") is not None
                and self.art_box.get() is not None
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastArt"] = self.art_path.cget("path")
            update_json()
            self.service.replace_bundle(DATA["name"][self.art_box.get()], "crd")
            self.select_card_art()
            show_message(
                MESSAGE["REPLACEMENT"], "Card Art texture replaced successfully!"
            )

    def replace_field(self):
        if (
                self.game_path.cget("path") is not None
                and self.field_path.cget("path") is not None
                and self.service.field_to_replace != -1
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastField"] = self.field_path.cget("path")
            update_json()
            self.service.replace_bundle(
                DATA["field"][self.service.field_to_replace],
                "fld",
                self.filter_field.state(),
            )
            self.fetch_target_thumbnails([["fields", fetch_field_thumb_list()]])
            show_message(
                MESSAGE["REPLACEMENT"], "Field texture replaced successfully!"
            )

    def replace_icon(self):
        if (
                self.game_path.cget("path") is not None
                and self.icon_path.cget("path") is not None
                and self.service.icon_to_replace != -1
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastIcon"] = self.icon_path.cget("path")
            update_json()
            size = 0
            for sprite in self.fetch_sprite_list(self.service.icon_to_replace):
                self.service.replace_bundle(sprite, "ico", False, False, size)
                size += 1
            self.fetch_target_thumbnails([["icons", self.service.fetch_icon_thumb_list()]])
            show_message(
                MESSAGE["REPLACEMENT"], "Icon texture replaced successfully!"
            )

    def replace_wallpaper(self):
        if (
                self.game_path.cget("path") is not None
                and self.wallpaper_path[0] is not None
                and self.wallpaper_box.current() is not None
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastWallpaper"][0] = self.wallpaper_path[0].cget("path")
            # TODO add support for wallpaper background replacement
            update_json()
            size = 0
            for part in DATA["wallpaper"][self.wallpaper_box.current()]:
                self.service.replace_bundle(part, "wpp", False, False, size)
                size += 1
            self.select_wallpaper_art()
            show_message(
                MESSAGE["REPLACEMENT"], "Wallpaper texture replaced successfully!"
            )

    def replace_home_bg(self):
        if (
                self.game_path.cget("path") is not None
                and self.home_path.cget("path") is not None
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastHome"] = self.home_path.cget("path")
            update_json()
            replace_unity3d_asset(
                "ShopBGBase02",
                convert_image(self.home_path.cget("path"), (1920, 1080)),
            )
            self.fetch_thumbnails()
            show_message(
                MESSAGE["REPLACEMENT"], "Home BG texture replaced successfully!"
            )

    def replace_face(self):
        if (
                self.game_path.cget("path") is not None
                and self.face_path.cget("path") is not None
        ):
            DATA["gamePath"] = self.game_path.cget("path")
            DATA["lastFace"] = self.face_path.cget("path")
            update_json()
            replace_unity3d_asset(
                DATA["types"][self.card_box.get()],
                convert_image(self.face_path.cget("path"), (704, 1024)),
                True,
            )
            self.select_face()
            show_message(
                MESSAGE["REPLACEMENT"], "Card face texture replaced successfully!"
            )

    def setup_sleeves(self, d):
        DATA["gamePath"] = self.game_path.cget("path")
        self.fetch_thumbnails()
        self.blocker_art.place(x=1025, y=1025)

    def extract_sleeve(self):
        if (
                self.game_path.cget("path") is not None
                and self.image_path.cget("path") is not None
                and self.service.sleeve_to_replace != -1
        ):
            self.service.extract_texture(
                DATA["adress"][self.service.sleeve_to_replace],
                DATA["adress"][self.service.sleeve_to_replace],
            )
            show_message(
                MESSAGE["EXTRACTION"],
                'Sleeve image exported to the "images" folder!',
            )

    def extract_art(self):
        if (
                self.game_path.cget("path") is not None
                and self.art_path.cget("path") is not None
                and self.art_box.get() is not None
        ):
            self.service.extract_texture(
                DATA["name"][self.art_box.get()], self.art_box.get()
            )
            show_message(
                MESSAGE["EXTRACTION"], 'Card art exported to the "images" folder!'
            )

    def extract_field(self):
        if self.game_path.cget("path") is not None and self.service.field_to_replace != -1:
            self.service.extract_texture(
                DATA["field"][self.service.field_to_replace],
                DATA["field"][self.service.field_to_replace],
            )
            show_message(
                MESSAGE["EXTRACTION"],
                'Field texture exported to the "images" folder!',
            )

    def extract_icon(self):
        if self.game_path.cget("path") is not None and self.service.icon_to_replace != -1:
            self.service.extract_texture(
                self.service.first_list[self.service.icon_to_replace],
                self.service.first_list[self.service.icon_to_replace],
            )
            show_message(
                MESSAGE["EXTRACTION"],
                'Icon image exported to the "images" folder!',
            )

    def extract_wallpaper(self):
        if (
                self.game_path.cget("path") is not None
                and self.wallpaper_box.current() is not None
        ):
            for wallpaper_part in DATA["wallpaper"][self.wallpaper_box.current()]:
                self.service.extract_texture(wallpaper_part, wallpaper_part)
            show_message(
                MESSAGE["EXTRACTION"],
                'Monster art exported to the "images" folder!',
            )

    def extract_home_bg(self):
        if self.game_path.cget("path") is not None:
            extract_unity3d_image("ShopBGBase02")
            show_message(
                MESSAGE["EXTRACTION"], 'Home BG exported to the "images" folder!'
            )

    def extract_face(self):
        if (
                self.game_path.cget("path") is not None
                and self.card_box.current() is not None
        ):
            extract_unity3d_image(DATA["types"][self.card_box.get()], True)
            show_message(
                MESSAGE["EXTRACTION"], 'Card face exported to the "images" folder!'
            )

    def swap_graves(self):
        if self.game_path.cget("path") is not None and -1 not in self.service.graves_to_replace:
            DATA["gamePath"] = self.game_path.cget("path")
            swap_bundles(
                [
                    DATA["grave"][0][self.service.graves_to_replace[0]],
                    DATA["grave"][0][self.service.graves_to_replace[1]]
                ]
            )
            swap_bundles(
                [
                    DATA["grave"][1][self.service.graves_to_replace[0]],
                    DATA["grave"][1][self.service.graves_to_replace[1]],
                ]
            )
            update_json()
            show_message(
                MESSAGE["SWAPPING"], "Grave meshes swapped successfully!"
            )
            self.fetch_target_thumbnails([["graves", fetch_swap_list("grave")]])

    def swap_bases(self):
        if self.game_path.cget("path") is not None and -1 not in self.service.bases_to_replace:
            DATA["gamePath"] = self.game_path.cget("path")
            swap_bundles(
                [
                    DATA["base"][0][self.service.bases_to_replace[0]],
                    DATA["base"][0][self.service.bases_to_replace[1]],
                ]
            )
            swap_bundles(
                [
                    DATA["base"][1][self.service.bases_to_replace[0]],
                    DATA["base"][1][self.service.bases_to_replace[1]],
                ]
            )
            update_json()
            show_message(
                MESSAGE["SWAPPING"], "Mate base meshes swapped successfully!"
            )
            self.fetch_target_thumbnails([["bases", fetch_swap_list("base")]])

    def swap_fields(self):
        if self.game_path.cget("path") is not None and -1 not in self.service.fields_to_replace:
            DATA["gamePath"] = self.game_path.cget("path")
            swap_bundles(
                [
                    DATA["full_field"][0][self.service.fields_to_replace[0]],
                    DATA["full_field"][0][self.service.fields_to_replace[1]],
                ]
            )
            swap_bundles(
                [
                    DATA["full_field"][1][self.service.fields_to_replace[0]],
                    DATA["full_field"][1][self.service.fields_to_replace[1]],
                ]
            )
            update_json()
            show_message(
                MESSAGE["SWAPPING"], "Field meshes swapped successfully!"
            )
            self.fetch_target_thumbnails(
                [
                    ["full_fields", fetch_swap_list("full_field")],
                    ["fields", fetch_field_thumb_list()],
                ]
            )

    def swap_mates(self):
        if self.game_path.cget("path") is not None and -1 not in self.service.mates_to_replace:
            DATA["gamePath"] = self.game_path.cget("path")
            swap_bundles(
                [
                    DATA["mate"][0][self.service.mates_to_replace[0]],
                    DATA["mate"][0][self.service.mates_to_replace[1]],
                ]
            )
            swap_bundles(
                [
                    DATA["mate"][1][self.service.mates_to_replace[0]],
                    DATA["mate"][1][self.service.mates_to_replace[1]],
                ]
            )
            update_json()
            show_message(
                MESSAGE["SWAPPING"], "Mate meshes swapped successfully!"
            )
            self.fetch_target_thumbnails([["mates", fetch_swap_list("mate")]])

    def copy_bundle(self, source_id) -> None:
        bundles = []

        match source_id:
            case "card_art":
                bundles = [DATA["name"][self.art_box.get()]]
            case "sleeve":
                bundles = [DATA["adress"][self.service.sleeve_to_replace]]
            case "mat":
                bundles = [DATA["field"][self.service.field_to_replace]]
            case "player_icon":
                bundles = DATA["icons"][
                    list(DATA["icons"].keys())[self.service.icon_to_replace]
                ]
            case "home_art":
                bundles = DATA["wallpaper"][self.wallpaper_box.current()]

        for bundle in bundles:
            copyfile(
                join(DATA["gamePath"], "0000", bundle[:2], bundle),
                join("bundles", source_id, bundle),
            )

        show_message(
            MESSAGE["COPYING"],
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
            DATA["background"] = self.art_path.cget("path")
            update_json()
            self.apply_background()
            show_message("Background", "App background set!")

    def reset_background(self):
        if self.game_path.cget("path") is not None:
            DATA["background"] = "empty"
            update_json()
            show_message("Background", "App background will reset on restart!")

    def run(self):
        self.mainwindow.mainloop()

    # === UNITY RELATED METHODS === #

    def fetch_thumbnails(self) -> None:
        """Fetches and creates the thumbnails used by the app"""

        if isdir(join(DATA["gamePath"], "0000", "00")):
            self.sleeves_img = fetch_sleeve_thumb_list()
            self.fields_img = fetch_field_thumb_list()
            self.graves_img = fetch_swap_list("grave")
            self.bases_img = fetch_swap_list("base")
            self.full_fields_img = fetch_swap_list("full_field")
            self.icons_img = self.service.fetch_icon_thumb_list()
            self.mates_img = fetch_swap_list("mate")
            self.home_bg_img = fetch_home_bg()

            ui_thumb_list = [
                [self.sleeves, self.sleeves_img],
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
            show_error(
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

    def fetch_sprite_list(self, index: int) -> list:
        """Fetches the sprite bundles related to the user given index"""

        sprite_list = []
        count = 0

        for li in DATA["icons"]:
            if count == index:
                sprite_list = DATA["icons"][li]
                sprite_list = self.sort_sprite_list(sprite_list)
                return sprite_list
            else:
                count += 1

        return sprite_list

    def select_image(self, index: int) -> None:
        """Assigns the index of the image selected by the user to the global 'self.sleeve_to_replace' variable and
        applies it to the selected card image"""

        sleeve = ImageTk.PhotoImage(
            self.service.fetch_image(DATA["adress"][index], "smp", False, (512, 746))
        )
        self.card.configure(image=sleeve)
        self.card.image = sleeve
        self.service.sleeve_to_replace = index

    def select_field_image(self, index: int) -> None:
        """Assigns the index of the image selected by the user to the global 'field_to_replace' variable and applies it
        to the selected field image"""

        self.service.field_to_replace = index
        field = ImageTk.PhotoImage(self.service.fetch_image(DATA["field"][index], "fld"))
        self.field.configure(image=field)
        self.field.image = field

    def select_grave_image(self, index: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'graves_to_replace' variable and applies it
        to the selected grave image"""

        self.service.graves_to_replace[pair] = index
        grave = ImageTk.PhotoImage(
            self.service.fetch_image(DATA["grave"][1][index], "smp", False, (200, 200))
        )
        self.graves_lbl[pair].configure(image=grave)
        self.graves_lbl[pair].image = grave

    def select_base_image(self, index: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'bases_to_replace' variable and applies it
        to the selected base image"""

        self.service.bases_to_replace[pair] = index
        base = ImageTk.PhotoImage(
            self.service.fetch_image(DATA["base"][1][index], "smp", False, (200, 200))
        )
        self.bases_lbl[pair].configure(image=base)
        self.bases_lbl[pair].image = base

    def select_full_field_image(self, index: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'self.fields_to_replace' variable and
        applies it to the selected field image"""

        self.service.fields_to_replace[pair] = index
        field = ImageTk.PhotoImage(
            self.service.fetch_image(DATA["full_field"][1][index], "smp", False, (200, 200))
        )
        self.full_fields_lbl[pair].configure(image=field)
        self.full_fields_lbl[pair].image = field

    def select_mate_image(self, index: int, pair: int) -> None:
        """Assigns the index of the image selected by the user to the global 'bases_to_replace' variable and applies it
        to the selected base image"""

        self.service.mates_to_replace[pair] = index
        mate = ImageTk.PhotoImage(
            self.service.fetch_image(DATA["mate"][1][index], "smp", False, (200, 200))
        )
        self.mates_lbl[pair].configure(image=mate)
        self.mates_lbl[pair].image = mate

    def select_icon_image(self, index: int) -> None:
        """Assigns the index of the image selected by the user to the global 'icon_to_replace' variable and applies it
        to the selected icon image"""

        self.service.icon_to_replace = index
        icon = ImageTk.PhotoImage(
            self.service.fetch_image(self.service.first_list[index], "smp", False, (200, 200))
        )
        self.icon.configure(image=icon)
        self.icon.image = icon

    def select_card_art(self) -> None:
        """Displays the card art of the card selected in the art combobox on-screen"""

        art = ImageTk.PhotoImage(
            self.service.fetch_image(
                DATA["name"][self.art_box.get()], "smp", False, (512, 512)
            )
        )
        self.card_art.configure(image=art)
        self.card_art.image = art

    def select_wallpaper_art(self) -> None:
        """Displays the art of the wallpaper selected in the wallpaper combobox on-screen, and its art ratio"""

        art = ImageTk.PhotoImage(
            self.service.fetch_image(
                DATA["wallpaper"][self.wallpaper_box.current()][0], "wpp"
            )
        )
        self.wallpaper_art.configure(image=art)
        self.wallpaper_art.image = art
        self.wallpaper_ratio.configure(
            text=str(int(art.width() / gcd(art.width(), art.height()))) + ":" + str(
                int(art.height() / gcd(art.width(), art.height())))
        )

    def select_face(self) -> None:
        """Displays the face of the card type selected in the face combobox on-screen"""

        face = ImageTk.PhotoImage(
            fetch_unity3d_image(
                DATA["types"][self.card_box.get()], (512, 746)
            )
        )
        self.face.configure(image=face)
        self.face.image = face

    def art_values(self, cache: list) -> None:
        """Filters the art combobox with the text inputted by the user"""

        i = self.art_box.get()
        db_list = [x for x in cache if i.upper() in x.upper()]
        self.art_box["values"] = sorted(db_list)

    def sort_sprite_list(self, sprite_list: list) -> list:
        """Sorts a given sprite list by image size"""

        for sprite in sprite_list:
            sprite_art = self.service.fetch_image(sprite, "spt")

            if sprite_art.width == 128:
                small_sprite = sprite
            elif sprite_art.width == 256:
                medium_sprite = sprite
            elif sprite_art.width == 512:
                large_sprite = sprite

        return [small_sprite, medium_sprite, large_sprite]

    def apply_background(self):
        """Applies the art of the user selected card art as the app's background"""

        bg_img = Image.open(DATA["background"]).resize((1400, 800))
        bg_img.putalpha(64)
        bg_img = ImageTk.PhotoImage(bg_img)

        for screen in self.bg:
            screen.configure(image=bg_img)
            screen.image = bg_img


if __name__ == "__main__":
    Root().run()
