<h1>floowandereeze-and-modding</h1>
<p align="center">
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
</p>
<p>This is a pure Python tool that is able to replace card sleeves, deluxe sleeves, card arts, icons, home arts and most fields in the Yu-Gi-Oh! Master Duel game with an user-given image, making the process of creating custom assets trivial. It's also able to swap mates and field assets.</p>

<h2>Building</h2>
<p>To build the app locally, create a Python venv with <code>Python -m venv venv</code> and install the development requirements with <code>pip install -r requirements.txt</code>. The requirements also include those used to update the app's data with the notebook found in the scrapping directory: bs4, jupyter, and selenium.</p>

<p>If all requirements are met running the build script with <code>.\build.ps1</code> should generate a working executable under the "dist" directory.</p>

<h2>Usage</h2>
<p>Download the tool from the 'releases' tab or Nexus Mods, then start "Floowandereeze & Modding.exe" found in the "Floowandereeze & Modding" folder.</p>

<p>Afterwards select your game directory by informing it's folder after pressing the first button. If the given folder is correct, the game's sleeves should appear as in the example bellow:</p>

<p align="center">
    <img src="https://i.ibb.co/q99f207/Captura-de-Tela-127.png">
</p>

<p>To update the app delete the old one and download the new one. The game path will have to be informed again.</p>

<p>Bellow are subsections describing how to utilize most of the app's functionalities, since many have identical steps, references to previous explanations are made for the sake of brevity</p>

<h3>Sleeves</h3>
<p>On the "sleeves" tab, click on the image of the sleeve you want to replace and it will appear on the right side of the screen. To replace the selected sleeve, inform the image to use by pressing the second button. For example, to replace the Xyz sleeve:</p>

<p align="center">
    <img src="https://i.ibb.co/Np4vNsq/Captura-de-Tela-129.png">
</p>

<p>Press the "Replace" button to replace the sleeve with your image (REPLACEMENT CANNOT BE REVERSED):</p>

<p align="center">
    <img src="https://i.ibb.co/Zz3KpDC/Captura-de-Tela-130.png">
</p>

<h3>Card Art</h3>
<p>Same steps as sleeve replacement but, instead of clicking on the image, select the name of the card to be replaced in the combo-box list in the "Card Art" tab after informing the game path.
To search for a specific card/archetype, write it's name in the combo-box field and open the list, it should be filtered with relevant results if the name was typed correctly.</p>

<p align="center">
    <img src="https://i.ibb.co/N7RNvsz/Captura-de-Tela-159.png">
</p>
<p align="center">
    <img src="https://i.ibb.co/MZ6Yq5Z/Captura-de-Tela-160.png">
</p>

<h3>Card Face</h3>
<p>Select what type of card to replace and inform the image to use, similar to sleeve replacement. Bear in mind that only the card frame will be replaced; text, icons and art aren't affected directly.</p>

<h3>Field</h3>
<p>Works exactly as sleeve replacement does but there is an added option to apply a filter on top of your image to highlight zone placement.</p>

<p>The extraction option will extract the image used by the game so to use it as a backup you need to either crop it or replace the asset directly.</p>

<p align="center">
    <img src="https://i.ibb.co/3hgn8SM/Captura-de-Tela-161.png">
</p>

<h4>Field Filter Editing</h4>
<p>This is only recommended if you know basic image editing. The app has the functionality to apply a filter on top of images when creating a field mod, this filter is made to be as generic as possible and some may want to change it, which is easy to do.</p>

<p>There are two files in the app's main folder: "base.png" and "base_inv.png" which are overlaid on the image to be used, editing these images will change the resulting filter accordingly. There are a few caveats to editing these files, which are the reason this functionality isn't in the app itself:</p>

<ul>
    <li>The edited filter will be lost if a backup is not generated before an app update, as the original images would overwrite the edited ones;</li>
    <li>As the filter image is simply pasted on top of the original image changing it's size would make the zones be misaligned;</li>
    <li>The texture being changed to apply the custom field image is used by multiple field parts, as can be seen by extracting it. This naturally means that if the filter is edited in unintended areas there could be side effects.</li>
</ul>

<h3>Icon</h3>
<p>Works exactly as sleeve replacement does. Please keep in mind that part of your image will be covered and cropped by the icon frame.</p>

<p align="center">
    <img src="https://i.ibb.co/dBFPcfN/Captura-de-Tela-162.png">
</p>

<h3>Home Art</h3>
<p>Select the original art to be replaced on the Combobox and inform your image. Currently the background of the art can't be modified through this tool, so consider that before replacing as that part of the art will be lost.</p>

<h4>Some aspects of home art replacement:</h4>
<ul>
    <li>Every home art has it's own proportions, off-screen parts, and empty space. Automatically fitting an user-given image is currently not viable, so images are pasted in the top-left corner of the home art and made to fit it's size;</li>
    <li>The images used by the game may be bigger than what is seen on the screen. In such cases if your image has the same proportions as the game's it will naturally have parts hidden too;</li>
    <li>If the image provided is smaller in pixel count than the game's art it may look small on-screen.</li>
</ul>

<p align="center">
    <img src="https://i.ibb.co/LQnP3XQ/Captura-de-Tela-168.png">
</p>

<h3>Home Background</h3>
<p>Simply inform the image to use and press the replace button. A preview of your current background is provided for reference.</p>

<h3>Field Assets and Mates Swapping</h3>
<p>Select both parts to be swapped using the left and right buttons of your mouse then click the "swap" button. An important point to consider is that the field texture replacement may not work properly if certain fields are swapped due to the difference between their UV maps. It should work properly again if the fields are returned to their original places before changing the texture.</p>

<h3>Notes</h3>
<ul>
    <li>As mentioned above, the tool can't undo edits, so make a backup if you want to reverse your mod;</li>
    <li>There is an "extract" option for every image so backups can be made easier, exported images are placed in the "images" folder inside the same folder containing the app's .exe;</li>
    <li>There is a "copy" option for most assets for easier redistribution and stronger backups. Copied asset bundles are placed in their corresponding subfolder inside the "bundles" folder found in the same folder containing the app's exe;</li>
    <li>Most visual aspects of the app, such as the layout and the background, have been made with it's starting window size in mind. While the window is made re-sizable for minimum accessibility standards, visual aspects may be compromised as a result;</li>
    <li>Both Card Faces and the Home Background are in the unity3d game file, so their replacements may be reverted if you download an external mod that change that file;</li>
    <li>The app should work normally through Wine for Linux users, a Linux binary could also be made based on the Pyinstaller command in the build script, but that has not been tested;</li>
    <li>Your image needs to be a .png or .jpg for it to properly work.</li>
</ul>

<h3>Known Issues</h3>
<ul>
    <li>There may be missing cards in the card art replacement. If you can't find a specific card, please contact me;</li>
    <li>The .exe was made for Windows 10 or above, there could be compatibility issues with earlier versions of Windows;</li>
    <li>Some features don't work with uncensored versions of the game as the asset names are different, a patch would have to be made (such as https://www.nexusmods.com/yugiohmasterduel/mods/384 by Sakuya_Saki).</li>
</ul>
