from os import remove
from os.path import join
from shutil import copyfile

from UnityPy import load as unity_load

from PIL import Image, ImageTk
from UnityPy.enums import TextureFormat

from util.constants import DATA, FILE, FIELD_FLIP_INDEX
from util.image_utils import slugify


def fetch_unity3d_image(path_id: str, aspect: tuple) -> Image.Image:
    """
        Fetch and resize an image from Unity3D resources.

        This function fetches an image with a specified Unity3D path ID, resizes it to the given aspect ratio, and converts it into RGB format.

        :param path_id: The path ID of the image in Unity3D resources.
        :type path_id: str
        :param aspect: A tuple representing the desired width and height for the image to be resized to.
        :type aspect: tuple
        :return: The resized and converted RGB image from Unity3D resources.
        :rtype: Image.Image
    """
    env = unity_load(
        join(DATA["gamePath"][:-18], "masterduel_Data", FILE["UNITY"])
    )

    for obj in env.objects:
        if obj.type.name == "Texture2D" and str(obj.path_id) == path_id:
            data = obj.read()
            img = data.image.resize(aspect)
            img.convert("RGB")
            img.name = "image.jpg"
            return img

    return Image.new("RGB", aspect)


def replace_unity3d_asset(asset: str, img: Image.Image, by_path_id=False) -> None:
    env = unity_load(
        join(DATA["gamePath"][:-18], "masterduel_Data", FILE["UNITY"])
    )

    if asset == 'ShopBGBase02':
        for obj in env.objects:
            if obj.type.name == "Sprite":
                data = obj.read()
                if asset == data.m_Name:
                    data.m_Rect.width, data.m_Rect.height = img.size
                    data.m_RD.textureRect.width, data.m_RD.textureRect.height = img.size
                    data.save()
                    break

    for obj in env.objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            if by_path_id and str(obj.path_id) == asset or asset == data.m_Name:
                data.m_Width, data.m_Height = img.size

                data.set_image(
                    img=img,
                    target_format=TextureFormat.RGBA32
                )

                data.save()
                break

    with open(
            join(DATA["gamePath"][:-18], "masterduel_Data", "data.unity3d"), "wb"
    ) as f:
        f.write(env.file.save())


def extract_unity3d_image(asset: str, by_id=False) -> None:
    """
        Extracts an image from Unity3D game data.

        This function locates either by asset ID or by name a texture
        object within Unity3D game data file and then saves it as a PNG file.

        :param asset: If `by_id` is False, it represents the name of the texture.
                      Otherwise, it is the texture's id.

        :param by_id: It is a flag used to switch between searching asset by its name or by its id.
                      By default, it is False, i.e., the function searches by name.

        :type asset: str

        :type by_id: bool, optional

        :returns: None. The function handles the saving of the image internally, therefore doesn't return anything.

        :raises FileNotFoundError: If the Unity3D game file path doesn't exist or the asset is not found within the game file.

        **Notes**

        The image is saved in a directory named "Images" or "images". Be sure this directory exists
        in the current working directory or else this function will raise an IOError.

        """
    for obj in unity_load(
            join(DATA["gamePath"][:-18], "masterduel_Data", FILE["UNITY"])
    ).objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            if by_id:
                if str(obj.path_id) == asset:
                    dest = join("Images", slugify(data.m_Name) + ".png")
                    img = data.image
                    img.save(dest)
                    break
            else:
                if asset == data.m_Name:
                    dest = join("images", slugify(data.m_Name) + ".png")
                    img = data.image
                    img.save(dest)
                    break


def fetch_sleeve_thumb_list() -> list[ImageTk.PhotoImage]:
    images_list = []
    for i in DATA["adress"]:
        f_path = join(DATA["gamePath"], "0000", i[:2], i)
        env = unity_load(f_path)
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                img = data.image.resize((128, 181))
                img.convert("RGB")
                img.name = FILE["IMAGE_NAME"]
                sleeve = ImageTk.PhotoImage(img)
                images_list.append(sleeve)
    return images_list


def fetch_icon_thumb_list() -> list[ImageTk.PhotoImage]:
    """
    Fetches a list of thumbnail images of icons from the specified game path.
    :return: A list of ImageTk.PhotoImage objects representing the thumbnail images of icons.
    """
    images_list = []
    for i in [DATA["icons"][a][0] for a in DATA["icons"]]:
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


def fetch_box_thumb_list() -> list[ImageTk.PhotoImage]:
    """
    Fetches a list of thumbnail images of icons from the specified game path.
    :return: A list of ImageTk.PhotoImage objects representing the thumbnail images of icons.
    """
    images_list = []
    for i in DATA["deck_box"]:
        for thumb in [i["small"], i["o_medium"]]:
            f_path = join(DATA["gamePath"], "0000", thumb[:2], thumb)
            env = unity_load(f_path)
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    img = data.image.resize((129, 129))
                    img.convert("RGB")
                    img.name = FILE["IMAGE_NAME"]
                    box = ImageTk.PhotoImage(img)
                    images_list.append(box)

    return images_list


def fetch_sleeve_dx_thumb_list() -> list[ImageTk.PhotoImage]:
    """Fetches the deluxe sleeve thumbnail list used by the app"""

    images_list = []
    for i in DATA["sleeveDeluxe"]:
        f_path = join(DATA["gamePath"], "0000", i[:2], i)
        env = unity_load(f_path)
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if "_1" in data.m_Name or "_2" in data.m_Name:
                    img = data.image.resize((187, 266))
                    img.convert("RGB")
                    img.name = FILE["IMAGE_NAME"]
                    sleeve = ImageTk.PhotoImage(img)
                    images_list.append(sleeve)

    return images_list


def fetch_home_bg() -> ImageTk.PhotoImage:
    env = unity_load(
        join(DATA["gamePath"][:-18], "masterduel_Data", FILE["UNITY"])
    )
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            if "ShopBGBase02" == data.m_Name:
                img = data.image.resize((1120, 630))
                img.convert("RGB")
                img.name = FILE["IMAGE_NAME"]
                bg = ImageTk.PhotoImage(img)
                return bg


def fetch_swap_list(part: str) -> list[ImageTk.PhotoImage]:
    """Fetches a swappable thumbnail list used by the app"""
    images_list = []
    for i in DATA[part][1]:
        f_path = join(DATA["gamePath"], "0000", i[:2], i)
        env = unity_load(f_path)
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                img = data.image
                img.convert("RGB")
                img.thumbnail((141, 141), Image.Resampling.LANCZOS)
                img.name = FILE["IMAGE_NAME"]
                part_thumb = ImageTk.PhotoImage(img)
                images_list.append(part_thumb)
    return images_list


def fetch_field_thumb_list() -> list[ImageTk.PhotoImage]:
    """Fetches the field thumbnail list used by the app"""
    images_list = []
    for i in DATA["field"]:
        f_path = join(DATA["gamePath"], "0000", i[:2], i)
        env = unity_load(f_path)
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if "01_BaseColor_near" in data.m_Name:
                    img = data.image
                    img.convert("RGB")
                    img.name = FILE["IMAGE_NAME"]
                    img_field = (
                        img.crop((0, 311, 2048, 1023)).rotate(180)
                        if len(images_list) < FIELD_FLIP_INDEX
                        else img.crop((0, 243, 2048, 955))
                    )
                    img_field.thumbnail(
                        (662, img_field.size[1]), Image.Resampling.LANCZOS
                    )
                    field = ImageTk.PhotoImage(img_field)
                    images_list.append(field)
    return images_list


def swap_bundles(bundles: list) -> None:
    """Swaps the content of two given bundles"""
    asset_1 = join(DATA["gamePath"], "0000", bundles[0][:2], bundles[0])
    asset_2 = join(DATA["gamePath"], "0000", bundles[1][:2], bundles[1])
    copyfile(asset_1, join(DATA["gamePath"], bundles[0]))
    copyfile(asset_2, asset_1)
    copyfile(join(DATA["gamePath"], bundles[0]), asset_2)
    remove(join(DATA["gamePath"], bundles[0]))


def prepare_environment(miss: bool, bundle: str) -> str:
    """returns the UnityPy environment path related to the bundle and game path given"""

    return (
        join(
            DATA["gamePath"][:-18],
            "masterduel_Data",
            "StreamingAssets",
            "AssetBundle",
            bundle[:2],
            bundle,
        )
        if miss
        else join(DATA["gamePath"], "0000", bundle[:2], bundle)
    )
