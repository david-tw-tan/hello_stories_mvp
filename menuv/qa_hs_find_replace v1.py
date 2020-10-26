#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

from sys import argv
from os.path import exists
import re
import fileinput

script = argv

print(f"Fetching index.html file")
print(f"...")


# Add audio tag to head of file + 2 unique ID tag for menu "button_click", "button_home" sfx
print(f"#1a. Find and replace - Adding audio tag at head of file")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('<div class="reveal">', '\n\t\t<!-- Required for playing JS audio, insert at top of <body> -->\n\t\t<audio id="audio"></audio>\n\t\t<audio id="sfx1" src="qa_audio/button_click.mp3" preload="auto"></audio>\n\t\t<audio id="sfx2" src="qa_audio/button_home.mp3" preload="auto"></audio>\n\n\t\t<div class="reveal">'), end='')
    print(f"Done!")
    print(f"...")


# Add play audio JS at end of file + pauseAll() into playAudio(el) function -->
print(f"#6a. Find and replace 6a - Adding play audio JS")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('<!-- Initialize the presentation -->', '\n\t\t<!-- JS script for playing onclick audio (include pauseAll onclick) -->\n\t\t<script>\n\t\t\tfunction play(){\n\t\t\t\tvar audio = document.getElementById("audio");\n\t\t\t\taudio.play();\n\t\t\t\t}\n\t\t\tfunction playAudio(el){\n\t\t\t\tvar audio = document.getElementById(\'audio\');\n\t\t\t\tvar source = el.getAttribute(\'data-src\');\n\t\t\t\t audio.src = source;\n\t\t\t\tpauseAll(); // add pause all function\n\t\t\t\taudio.play();\n\t\t\t}\n\t\t</script>\n\n\t\t<!-- Initialize the presentation -->'), end='')

# Add play audio JS for book menu, required as menu sfx are href links, includes separate playsfx_X methods for "button_click" and "button_home" sfx
print(f"#6a. Find and replace 6a - Adding play audio JS")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('<!-- Initialize the presentation -->', '<script>\n// Working menu sfx method, takes 1 argument for url. Note: requires defining unique audio IDs, one method per sfx ID\n// sfx1 "button click" \nfunction playsfx_1(url) {\n\tvar sound = document.getElementById("sfx1");\n\tsound.play();\n\tsound.addEventListener(\'ended\', function () {\n\t\tlocation.href = url;\n\t});\n}\n// sfx2 "button home" \nfunction playsfx_2(url) {\n\tvar sound = document.getElementById("sfx2");\n\tsound.play();\n\tsound.addEventListener(\'ended\', function () {\n\t\tlocation.href = url;\n\t});\n}\n</script>\n\n\n\t\t<!-- Initialize the presentation -->'), end='')


# Add onclick tag whereever there is a id="playsfx_ ..." for playing all menu related sfx
print(f"#2. Find and replace 2 - Adding onclick to existing pre-inserted audio tags -- qa_audio folder")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('id="playsfx_', 'onclick="playsfx_'), end='')
    print(f"Done!")
    print(f"...")


# At end of <body>, add 2 pauseAll() scripts for when there is "onclick" audio or "slide change" event -->
# At same time also add GA event tracking whenever there is a page turn
print(f"#6b. Find and replace 6b - pauseAll() JS")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('<!-- Initialize the presentation -->', '\n\t\t<!-- Stop all current audio when new one plays -->\n\t\t\t<script>\n\t\t\t\tvar audios = document.getElementsByTagName("audio");\n\t\t\t\tfunction pauseAll(){\n\t\t\t\t\tvar self = this;\n\t\t\t\t\t[].forEach.call(audios, function (i){\n\t\t\t\t\t\ti !== self && i.pause();\n\t\t\t\t\t})\n\t\t\t\t}\n\t\t\t\t</script>\n\n\t\t\t<!-- AddEventListener for slide change event, initiate pauseAll + GA event tracking when this happens -->\n\t\t\t\t<script>\n\t\t\t\tReveal.addEventListener(\'slidechanged\', function() {\n\t\t\t\t\tpauseAll();\n\t\t\t\tgtag(\'event\', \'turnpage\'); // add GA event tracking for "turnpage"\n\t\t\t\t} );\n\t\t\t\t</script>\n\n\n\n\t\t<!-- Initialize the presentation -->'), end='')


# Add onclick tag to pre-inserted audio urls from QA_AUDIO folder
print(f"#2. Find and replace 2 - Adding onclick to existing pre-inserted audio tags -- qa_audio folder")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('data-src="qa_audio/', 'onclick="playAudio(this);" data-src="qa_audio/'), end='')
    print(f"Done!")
    print(f"...")


# Add onclick tag to pre-inserted audio urls from REPLIES folder
print(f"#4. Find and replace 4 - Adding onclick to existing pre-inserted audio tag -- replies folder")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('data-src="replies/', 'onclick="playAudio(this)" data-src="replies/'), end='')
    print(f"Done!")
    print(f"...")


# Add onclick tag to pre-inserted audio urls from ANSWERS folder
print(f"#3. Find and replace 3 - Adding onclick to existing pre-inserted audio tag -- answers folder")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('data-src="answers/', 'onclick="playAudio(this)" data-src="answers/'), end='')
    print(f"Done!")
    print(f"...")


# Add PLACEHOLDERS for 1) slide numbers AND 2) vocal narration audio url at start of each <section>
# 3) add code for replay button AND with "pop" ID animation
# Note 1 when replacing with captured tokens, replacement parameter must be preceded by 'r'
# Note 2 when <section> class = "stack", we do NOT add tags.
# XXX = slide number placeholder
# YYY = narration audio file placeholder

print(f"#6. Adding <section> slide number place holders AND vocal narration URL.")
print(f"...")

file = open('index.html', "r")
text = file.read()
file.close()
file = open('index.html', "w")
file.write(re.sub('<section data(.+?)>',r'\n\n<section data\1>\n<!-- ** Start of SLIDE < XXX > ** -->\n<audio data-autoplay="" data-paused-by-reveal="" data-lazy-loaded="" src="vocals/YYY.mp3"></audio>\n\n<div class="sl-block" data-block-type="image" style="min-width: 4px; min-height: 4px; width: 198px; height: 198px; left: -22px; top: 1270px;">\n\t<div class="sl-block-content" style="z-index: 50;" onclick="playAudio(this)" data-src="vocals/YYY.mp3" id="pop"><img style="" data-natural-width="242" data-natural-height="241" data-lazy-loaded="" src="qa_audio/replay_button.png"/>\t</div></div>\n\n',text))
file.close()

# Update placeholder XXX value for SLIDE NUMBER with actual slide number
print(f"#7. Updating <section> slide number placeholders with actual slide number.")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    slide = 1
    subslide = 0
    for line in file:
        if 'class="stack"' in line:
            subslide = 1
        if '</section></section>' in line:
            subslide = 0
            slide = slide + 1
        if '<section ' in line:
            if subslide > 0:
                text = 'Start of SLIDE < ' + str(slide) + '-' + str(subslide-1) + ' >' #slide number format for nested slides
                subslide = subslide + 1
            else:
                text = 'Start of SLIDE < ' + str(slide) + ' >' #slide number format for normal slides
                slide = slide + 1
        print(line.replace('Start of SLIDE < XXX >', text), end='')
print(f"...")
print(f"Done!")

# Update placeholder YYY value in VOCALS audio URL with correct slide number
print(f"#8. Updating narration audio URLs to match correct slide number.")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        if '** Start of SLIDE <' in line:
            start_pos = line.find('< ')
            end_pos = line.find(' >')
            text = 'src="vocals/' + line[start_pos+2:end_pos] + '.mp3"'
        print(line.replace('src="vocals/YYY.mp3"', text), end='')

# Update placeholder XXX value in REPLIES audio URL with correct slide number
print(f"#8. Updating replies audio URLs to match correct slide number.")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        if '** Start of SLIDE <' in line:
            start_pos = line.find('< ')
            end_pos = line.find(' >')
            text = 'src="replies/' + line[start_pos+2:end_pos]
        print(line.replace('src="replies/XXX', text), end='')
print(f"...")
print(f"Done!")

# Update placeholder XXX value in HINTS audio URL with correct slide number
print(f"#9. Updating replies hints URLs to match correct slide number.")
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        if '** Start of SLIDE <' in line:
            start_pos = line.find('< ')
            end_pos = line.find(' >')
            text = 'src="hints/' + line[start_pos+2:end_pos]
        print(line.replace('src="hints/XXX', text), end='')
print(f"...")
print(f"Done!")

# For narration onclick replay link
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('onclick="playAudio(this)" data-src="vocals/', 'onclick="playAudio(this)" data-src="vocals/'), end='')
    print(f"Done!")
    print(f"...")

# disable revealjs disable touch navigation for mobile devices (needed bc swiping doesn't activate autoplay)
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('controls: true,', 'controls: true,\n\t\t\t\ttouch: false,'), end='')
    print(f"Done!")
    print(f"...")

# change all href links to open in same window
print(f"...")
with fileinput.FileInput('index.html', inplace=True) as file:
    for line in file:
        print(line.replace('target="_blank"', 'target="_self"'), end='')
    print(f"Done!")
    print(f"...")

print(f"...")
print(f"index.html file has been updated!")
print(f"...")
print(f"END OF PROGRAM")
print(f"")
