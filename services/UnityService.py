from os.path import join

from PIL import Image, ImageTk

from util.constants import DATA, FILE, FIELD_FLIP_INDEX, PROJECT_PATH
from util.image_utils import convert_image, add_sleeve_border, slugify
from util.unity_utils import prepare_environment
from UnityPy import load as unity_load


class UnityService:
    """
    UnityService class provides methods for fetching and replacing images from Unity asset bundles.
    """

    def __init__(self):
        self._icon_to_replace: int = -1
        self._field_to_replace: int = -1
        self._sleeve_to_replace: int = -1
        self._graves_to_replace: list[int] = [-1, -1]
        self._bases_to_replace: list[int] = [-1, -1]
        self._fields_to_replace: list[int] = [-1, -1]
        self._mates_to_replace: list[int] = [-1, -1]
        self._first_list: list = [DATA["icons"][a][0] for a in DATA["icons"]]

    def fetch_image(
            self, bundle: str, aspect: str, miss=False, simple_aspect=(0, 0)
    ) -> Image.Image:
        """
        Fetches an image from a Unity asset bundle.

        :param bundle: A string representing the name of the asset bundle.
        :param aspect: A string representing the aspect of the image to fetch.
        :param miss: A bool indicating whether a previous fetch attempt failed (default: False).
        :param simple_aspect: A tuple representing the dimensions of the image to fetch when aspect is "smp"
        (default: (0, 0)).

        :return: An instance of PIL Image.Image representing the fetched image.
        """
        env = unity_load(prepare_environment(miss, bundle))

        for obj in env.objects:
            found = False
            if obj.type.name == "Texture2D":
                data = obj.read()

                if aspect == "smp":
                    img = data.image.resize(simple_aspect, Image.Resampling.LANCZOS)
                    found = True
                elif aspect == "wpp":
                    img = data.image
                    img.thumbnail((760, 760), Image.Resampling.LANCZOS)
                    found = True
                elif aspect == "fld":
                    if "01_BaseColor_near" in data.name:
                        img = data.image
                        if self.field_to_replace < FIELD_FLIP_INDEX:
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

    def fetch_icon_thumb_list(self) -> list[ImageTk.PhotoImage]:
        """

        Fetches a list of thumbnail images of icons from the specified game path.

        :return: A list of ImageTk.PhotoImage objects representing the thumbnail images of icons.

        """
        images_list = []

        for i in self.first_list:
            f_path = join(DATA["gamePath"], "0000", i[:2], i)
            env = unity_load(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    img = data.image.resize((129, 129))
                    img.convert("RGB")
                    img.name = FILE["IMAGE_NAME"]
                    icon = ImageTk.PhotoImage(img)
                    images_list.append(icon)

        return images_list

    def replace_bundle(
            self, bundle: str, asset: str, filtered="empty", miss=False, size=-1
    ) -> None:
        """

        Replace Bundle

        Replaces an asset in a Unity bundle file with a new asset.

        Parameters:
        - bundle (str): The path to the Unity bundle file.
        - asset (str): The type of asset to replace. Possible values are "slv", "crd", "ico", "wpp", and "fld".
        - filtered (optional str): The filter type for the asset. Default is "empty".
        - miss (optional bool): Specifies whether to skip missing assets. Default is False.
        - size (optional int): The size of the new asset. Default is -1.

        Returns:
        None

        """
        f_path = prepare_environment(miss, bundle)
        env = unity_load(f_path)

        found = False

        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()

                if asset == "slv":
                    img = (
                        add_sleeve_border(
                            convert_image(DATA["lastImage"], (480, 700))
                        )
                        if "selected" in filtered
                        else convert_image(DATA["lastImage"], (480, 700))
                    )
                    found = True
                elif asset == "crd":
                    img = convert_image(DATA["lastArt"], (512, 512))
                    found = True
                elif asset == "ico":
                    if size == 0:
                        s = 128
                    elif size == 1:
                        s = 256
                    elif size == 2:
                        s = 512
                    img = Image.open(DATA["lastIcon"]).resize((s, s))
                    found = True
                elif asset == "wpp":
                    if size == 0:
                        img = Image.open(DATA["lastWallpaper"][0])
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
                    if self.field_to_replace < FIELD_FLIP_INDEX:
                        mat = Image.open(DATA["lastField"]).rotate(180)
                    else:
                        mat = Image.open(DATA["lastField"])
                    while mat.size[0] < 2048 or mat.size[1] < 712:
                        mat = mat.resize((mat.size[0] * 2, mat.size[1] * 2))
                    mat.thumbnail((2048, mat.size[1]), Image.Resampling.LANCZOS)
                    mat_fit = mat.crop((0, 0, 2048, 712))
                    if self.field_to_replace < FIELD_FLIP_INDEX:
                        img.paste(mat_fit, (0, 311))
                    else:
                        img.paste(mat_fit, (0, 243))
                    if "selected" in filtered:
                        if self.field_to_replace < FIELD_FLIP_INDEX:
                            base = Image.open(f'{PROJECT_PATH}/res/base.png')
                        else:
                            base = Image.open(f'{PROJECT_PATH}/res/base_inv.png')
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

    def extract_texture(self, bundle: str, name: str, miss=False) -> None:
        """
        Extracts a texture from a Unity bundle.

        :param bundle: The name of the Unity bundle.
        :param name: The name of the texture to extract.
        :param miss: A boolean value indicating if the extraction failed to find the bundle.
        :return: None
        """
        found = False

        for obj in unity_load(prepare_environment(miss, bundle)).objects:
            if obj.type.name == "Texture2D":
                data = obj.read()

                if name == DATA["field"][self.field_to_replace]:
                    if "01_BaseColor_near" in data.name:
                        found = True
                else:
                    found = True

                if found:
                    dest = join("images", slugify(name) + ".png")

                    img = data.image
                    img.save(dest)
                    break
        else:
            return self.extract_texture(bundle, name, True)

    @property
    def field_to_replace(self) -> int:
        return self._field_to_replace

    @field_to_replace.setter
    def field_to_replace(self, value: int):
        self._field_to_replace = value

    @property
    def sleeve_to_replace(self) -> int:
        return self._sleeve_to_replace

    @sleeve_to_replace.setter
    def sleeve_to_replace(self, value: int):
        self._sleeve_to_replace = value

    @property
    def icon_to_replace(self) -> int:
        return self._icon_to_replace

    @icon_to_replace.setter
    def icon_to_replace(self, value: int):
        self._icon_to_replace = value

    @property
    def graves_to_replace(self) -> list[int]:
        return self._graves_to_replace

    @graves_to_replace.setter
    def graves_to_replace(self, value: list[int]):
        self._graves_to_replace = value

    @property
    def bases_to_replace(self) -> list[int]:
        return self._bases_to_replace

    @bases_to_replace.setter
    def bases_to_replace(self, value: list[int]):
        self._bases_to_replace = value

    @property
    def fields_to_replace(self) -> list[int]:
        return self._fields_to_replace

    @fields_to_replace.setter
    def fields_to_replace(self, value: list[int]):
        self._fields_to_replace = value

    @property
    def mates_to_replace(self) -> list[int]:
        return self._mates_to_replace

    @mates_to_replace.setter
    def mates_to_replace(self, value: list[int]):
        self._mates_to_replace = value

    @property
    def first_list(self) -> list:
        return self._first_list

    @first_list.setter
    def first_list(self, value: list):
        self._first_list = value
