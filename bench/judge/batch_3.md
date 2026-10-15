

========== ITEM 004_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/004_terminal.png
----- GROUND TRUTH -----
$ curl -s https://api.github.com/repos/basecamp/omarchy | jq .stargazers_count
18342
----- OUTPUT A -----
$ curl -s https://api.github.com/repos/basecamp/omarchy l jq .stargazers_count
18342
----- OUTPUT B -----
$ curl -s https://api.github.com/repos/basecamp/omarchy | jg .stargazers_count
18342


========== ITEM 008_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/008_terminal.png
----- GROUND TRUTH -----
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            15Gi       8.3Gi       758Mi       806Mi       8.0Gi       7.0Gi
Swap:          4.0Gi       512Mi       3.5Gi
----- OUTPUT A -----
$ free -h

total        used        free      shared buff/cache available
Mem:            1561       8.361       758M1       806M1       8.061       7.061
Swap:          4.06       512i       3.561
----- OUTPUT B -----
$ free -h
              total       used       free     shared buff/cache available
Mem:          15Gi      8.3Gi      758Mi      806Mi      8.0Gi      7.0Gi
Swap:         4.0Gi      512Mi      3.5Gi


========== ITEM 012_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/012_code.png
----- GROUND TRUTH -----
SELECT u.id, u.email, COUNT(o.id) AS orders
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 3;
----- OUTPUT A -----
SELECT u.id, u.email, COUNT(o.id) AS orders
FROM users U
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 3;
----- OUTPUT B -----
SELECT v.id, u.email, COUNT(o.id) AS orders
FROM users u

LEFT JOIN orders o ON o.user_id = v.id
WHERE v.created_at >= '2024-81-01"

GROUP BY v.id, v.email

HAVING COUNT(o0.id) > 3;


========== ITEM 016_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/016_code.png
----- GROUND TRUTH -----
package main

import "fmt"

func main() {
    m := map[string]int{"a": 1, "b": 2}
    for k, v := range m {
        fmt.Printf("%s=%d\n", k, v)
    }
}
----- OUTPUT A -----
package main

import "fmt"

func main() {
    m := map[string]int{"a": 1, "b": 2}
    for k, v := range m {
        fmt.Printf("%s=%d\n", k, v)
----- OUTPUT B -----
package main
import "fmt"
func main() §
m := map[string]int{"a": 1, "b": 2%
for k, v := range m {
fmt. Printf("%s=%d\n", k, v)
3
¥


========== ITEM 020_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/020_code.png
----- GROUND TRUTH -----
o.bind("SUPER + CTRL + PRINT", "Extract text (OCR)", "omarchy-capture-text")
hl.unbind("SUPER + SHIFT + F")
o.window("org.gnome.Calculator", { tag = "+floating-window" })
----- OUTPUT A -----
o.bind("SUPER + CTRL + PRINT", "Extract text (OCR)", "omarchy-capture-text")
hl.unbind("SUPER + SHIFT + F")
o.window("org.gnome.Calculator", { tag = "+floating-window" })
----- OUTPUT B -----
0.bind("SUPER + CTRL + PRINT", "Extract text (OCR)", "omarchy-capture-text")
h1l.unbind("SUPER + SHIFT + F")
o.window("org.gnome.Calculator", { tag = "+floating-window" })


========== ITEM 024_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/024_prose.png
----- GROUND TRUTH -----
Latency matters more than throughput when a person is waiting for the result.
Good error messages explain what happened, why, and what to do next.
Compression trades CPU time for smaller files and faster transfers.
A tiling window manager arranges windows so that nothing ever overlaps.
The archive contains 1,284 photos taken between 2019 and 2024.
----- OUTPUT A -----
Latency matters more than throughput when a person is waiting for the result.
Good error messages explain what happened, why, and what to do next.
Compression trades CPU time for smaller files and faster transfers.

A tiling window manager arranges windows so that nothing ever overlaps.
The archive contains 1,284 photos taken between 2019 and 2024.
----- OUTPUT B -----
Latency matters more than throughput when a person is waiting for the result.
Good error messages explain what happened, why, and what to do next.
Compression trades CPU time for smaller files and faster transfers.
A tiling window manager arranges windows so that nothing ever overlaps.
The archive contains 1,284 photos taken between 2019 and 2024.


========== ITEM 028_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/028_prose.png
----- GROUND TRUTH -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Keep your dotfiles in version control so a new machine takes minutes, not days.
She opened the terminal, typed a single command, and the build finally passed.
Backups are only useful if you have actually tried restoring from them.
----- OUTPUT A -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.

Keep your doffiles in version control so a new machine takes minutes, not days.
She opened the terminal, typed a single command, and the build finally passed.
Backups are only useful if you have actually tried restoring from them.
----- OUTPUT B -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Keep your dotfiles in version control so a new machine takes minutes, not days.
She opened the terminal, typed a single command, and the build finally passed.
Backups are only useful if you have actually tried restoring from them.


========== ITEM 032_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/032_ui.png
----- GROUND TRUTH -----
Search settings Keyboard
Layout: US Repeat rate
Caps Lock as Ctrl
----- OUTPUT A -----
Search settings               Keyboard

Layout: US                   Repeat rate

Caps Lock as Ctrl
----- OUTPUT B -----
  Search settings           |  Keyboard                  |
   Layout: US                 |  Repeat rate                |
  Caps Lock as Ctrl        |


========== ITEM 036_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/036_ui.png
----- GROUND TRUTH -----
Inbox (23) Starred
Sent Drafts
Spam Compose
----- OUTPUT A -----
Inbox (23)                           Starred
Sent                                  Drafts
Spam                                             Compose
----- OUTPUT B -----
Inbox (23)             Starred
Sent                Drafts
Spam                Compose


========== ITEM 040_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/040_small_text.png
----- GROUND TRUTH -----
Wayland compositors handle input, output and window management in one process.
Small, frequent commits make it far easier to find the change that broke things.
Readable code is written for the next person, who is usually you.
If the fan is loud, check which process is using the most CPU first.
Screen readers depend on applications exposing correct accessibility labels.
----- OUTPUT A -----
Wayland compositors handle input, output and window management in one process.
Small, frequent commits make it far easier to find the change that broke things.
Readable code is written for the next person, who is usually you.

If the fan is loud, check which process is using the most CPU fist.

Screen readers depend on applications exposing correct accessibility labels.
----- OUTPUT B -----
Wayland compositors handle input, output and window management in one process.
Small, frequent commits make it far easier to find the change that broke things.
Readable code is written for the next person, who is usually you.
If the fan is loud, check which process is using the most CPU first.
Screen readers depend on applications exposing correct accessibility labels.


========== ITEM 044_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/044_small_text.png
----- GROUND TRUTH -----
Keep your dotfiles in version control so a new machine takes minutes, not days.
The meeting moved to Thursday at 3:30 PM because the projector was broken.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
Write the test first, watch it fail, then make it pass with the simplest code.
Our support team replies within 24 hours, including weekends and holidays.
----- OUTPUT A -----
Keep your dotfiles in version control so a new machine takes minutes, not days.
The meeting moved to Thursday at 3:30 PM because the projector was broken.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
Write the test first, watch it fail, then make it pass with the simplest code.
Our support team replies within 24 hours, including weekends and holidays.
----- OUTPUT B -----
Keep your dotfiles in version control so a new machine takes minutes, not days.
‘The meeting moved to Thursday at 3:30 PM because the projector was broken.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.

Write the test first, watch it fail, then make it pass with the simplest code.

Our support team replies within 24 hours, including weekends and holidays.


========== ITEM 048_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/048_low_contrast.png
----- GROUND TRUTH -----
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
The library closes at 9 PM on weekdays and at noon on Saturdays.
Readable code is written for the next person, who is usually you.
Keep your dotfiles in version control so a new machine takes minutes, not days.
----- OUTPUT A -----
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
The library closes at 9 PM on weekdays and at noon on Saturdays.
Readable code is written for the next person, who is usually you.
Keep your dotfiles in version control so a new machine takes minutes, not days.
----- OUTPUT B -----
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.

The library closes at 9 PM on weekdays and at noon on Saturdays.

Readable code is written for the next person, who is usually you.

Keep your dofies in version control so a new machine takes minutes, not days.


========== ITEM 052_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/052_low_contrast.png
----- GROUND TRUTH -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
The quick brown fox jumps over the lazy dog near the riverbank.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
----- OUTPUT A -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
The quick brown fox jumps over the lazy dog near the riverbank.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
----- OUTPUT B -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.

The quick brown fox jumps over the lazy dog near the riverbank.

Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.


========== ITEM 056_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/056_table.png
----- GROUND TRUTH -----
PID USER CPU% MEM% COMMAND
1043 user 12.4 3.1 chromium
877 root 4.0 0.8 Hyprland
2210 user 1.7 1.2 alacritty
15 root 0.0 0.0 kthreadd
----- OUTPUT A -----
PID     USER CPU% MEM% COMMAND
1043 user 12.4 3.1     chromium
877     root 4.0     0.8     Hyprland
2210 user 1.7     1.2     alacritty
15      root 0.0     0.0     kthreadd
----- OUTPUT B -----
PID USER CPU% MEM% COMMAND
1043 user 12.4 3.1 chromium
877 root 4.0 0.8 Hyprland
2210 user 1.7 1.2 alacritty
15   root 0.0 0.0 kthreadd


========== ITEM 060_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/060_table.png
----- GROUND TRUTH -----
Name Role Location Since
Alice Moreau Engineer Paris 2019
Bob Chen Designer Taipei 2021
Carlos Ruiz Manager Madrid 2017
Dana Kim Analyst Seoul 2023
----- OUTPUT A -----
Name         Role     Location Since
Alice Moreau Engineer Paris     2019
Bob Chen      Designer Taipei    2021
Carlos Ruiz   Manager   Madrid    2017
Dana Kim     Analyst   Seoul     2023
----- OUTPUT B -----
Name        Role    Location Since
Alice Moreau Engineer Paris   2019
Bob Chen    Designer Taipei 2021
Carlos Ruiz Manager Madrid 2017
Dana Kim    Analyst Seoul   2023


========== ITEM 064_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/064_identifiers.png
----- GROUND TRUTH -----
https://www.pixel-cloud.org/docs/v4/getting-started?ref=nav#install
/home/user/.config/cloud/pixel_6.toml
cloud.pixel90@example.com
Server: 174.84.7.44:443
API_KEY=demo-X6f6Ybd57670ZYb5Zfa393Z9
----- OUTPUT A -----
https: //www.pixel-cloud.org/docs/v4/getting-started?ref=nav#install
/home/user/.config/cloud/pixel_6.toml

cloud.pixel96@example.com

Server: 174.84.7.44:443

API_KEY=demo-X6f6Ybd57670ZYh52fa39329
----- OUTPUT B -----
https://www.pixel-cloud.org/docs/v4/getting-started?ref=nav#install
/home/user/.config/cloud/pixel_6.toml
cloud.pixel90@example.com
Server：174.84.7.44:443
API_KEY=demo-X6f6Ybd57670ZYb5Zfa393Z9


========== ITEM 068_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/068_identifiers.png
----- GROUND TRUTH -----
Server: 216.71.159.100:22
commit 21f05184610f9a645403753f2775d2cc664a05b6
API_KEY=demo-9Y34fQd9a4302c6321Z96Xf8
UUID: a3f5f54b-ab08-29d2-362d-a2a6e3eca5c7
/home/user/.config/delta/ember_18.toml
https://www.ember-delta.org/docs/v2/getting-started?ref=nav#install
https://github.com/delta-ember/river-8/pull/6660
----- OUTPUT A -----
Server: 216.71.159.100:22

commit 21f05184610f9a645403753F2775d2cc664a05b6
API_KEY=demo-9Y34fQd9a4302¢c63217296Xf8

UUID: a3f5f54b-ah08-29d2-362d-a2abe3ecasbc7
/home/user/.config/delta/ember_18.toml
https://www.ember-delta.org/docs/v2/getting-started?ref=nav#install
https://github.com/delta-ember/river-8/pull/6660
----- OUTPUT B -----
Server：216.71.159.100:22
commit 21f05184610f9a645403753f2775d2cc664a05b6
API_KEY=demo-9Y34fQd9a4302c6321Z96Xf8
UUID：a3f5f54b-ab08-29d2-362d-a2a6e3eca5c7
/home/user/.config/delta/ember_18.toml
https://www.ember-delta.org/docs/v2/getting-started?ref=nav#install
https://github.com/delta-ember/river-8/pull/6660


========== ITEM 072_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/072_identifiers.png
----- GROUND TRUTH -----
API_KEY=demo-4Q9512d013e1YaXYQf6X72e3
/home/user/.config/bravo/alpha_49.toml
https://github.com/bravo-alpha/pixel-3/pull/1244
https://www.alpha-bravo.org/docs/v3/getting-started?ref=nav#install
commit 3dcfd4a43ca8e4d035b0c2273ecfd564271dc27f
----- OUTPUT A -----
API_KEY=demo-4Q9512d013e1YaXYQf6X72e3
/home/user/.config/bravo/alpha_49.toml
https://github.com/bravo-alpha/pixel-3/pull/1244
https://www.alpha-bravo.org/docs/v3/getting-started?ref=nav#install
commit 3dcfd4a43ca8e4d035b0c2273ecfd564271dc27f
----- OUTPUT B -----
API_KEY=demo-4Q9512d013e1YaXYQf6X72e3
/home/user/.config/bravo/alpha_49.toml
https://github.com/bravo-alpha/pixel-3/pull/1244

https: //www.alpha-bravo.org/docs/v3/getting-started?ref=nav#install
commit 3dcfd4ad43ca8ed4dB035b0c2273ecfd564271dc27f


========== ITEM 076_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/076_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2025-48843
Date: 07/05/2026
Amount due: $3,113.17
Phone: +1 (826) 258-4006
IBAN: DE57 1995 1353 7461 7995 93
Version 2.1.79 (build 89565)
Order total: 91 items, 12.78 kg
Tracking: 1ZLSNP0WHTC7R58RF3
----- OUTPUT A -----
Invoice No. INV-2025-48843

Date: 07/05/2026

Amount due: $3,113.17

Phone: +1 (826) 258-4006

IBAN: DE57 1995 1353 7461 7995 93
Version 2.1.79 (build 89565)

Order total: 91 items, 12.78 kg
Tracking: 1ZLSNPOWHTC7R58RF3
----- OUTPUT B -----
Invoice No. INV-2025-48843
Date: 07/05/2026
Amount due: $3,113.17
Phone: +1 (826) 258-4006
IBAN: DE57 1995 1353 7461 7995 93
Version 2.1.79 (build 89565)
Order total: 91 items, 12.78 kg
Tracking: 1ZLSNP0WHTC7R58RF3


========== ITEM 080_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/080_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2026-90102
Date: 03/08/2023
Amount due: $5,019.82
Phone: +1 (642) 256-9316
IBAN: DE78 9052 7854 1689 9978 46
----- OUTPUT A -----
Invoice No. INV-2026-90102

Date: 03/08/2023

Amount due: $5,019.82

Phone: +1 (642) 256-9316

IBAN: DE78 9052 7854 1689 9978 46
----- OUTPUT B -----
Invoice No. INV-2026-90102
Date：03/08/2023
Amount due：$5,019.82
Phone：+1 （642) 256-9316
IBAN: DE78 9052 7854 1689 9978 46


========== ITEM 084_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/084_accented.png
----- GROUND TRUTH -----
Æble, øl og smørrebrød er typisk dansk mad.
Über den Wolken muss die Freiheit wohl grenzenlos sein.
Bitte schließen Sie die Tür, bevor Sie gehen.
Le café de la gare est fermé le dimanche après-midi.
Où est la bibliothèque la plus proche, s'il vous plaît ?
----- OUTPUT A -----
AEble, øl og smørrebrød er typisk dansk mad.
Über den Wolken muss die Freiheit wohl grenzenlos sein.
Bitte schließen Sie die Tür, bevor Sie gehen.
Le café de la gare est fermé le dimanche après-midi.
Où est la bibliothèque la plus proche, s'il vous plaît ?
----- OUTPUT B -----
ZEble, ol og smorrebrod er typisk dansk mad.

Uber den Wolken muss die Freiheit wohl grenzenlos sein.
Bitte schlieBen Sie die Tir, bevor Sie gehen.

Le café de la gare est fermé le dimanche aprés-midi.

Ou est la bibliothéque la plus proche, s'il vous plait ?


========== ITEM 088_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/088_accented.png
----- GROUND TRUTH -----
Æble, øl og smørrebrød er typisk dansk mad.
Bitte schließen Sie die Tür, bevor Sie gehen.
São Paulo é a maior cidade do Brasil em população.
Ça coûte 12,50 € pour deux crêpes et un thé glacé.
----- OUTPUT A -----
Able, ol og smorrebrad er typisk dansk mad.

Bitte schlieBen Sie die Tiir, bevor Sie gehen.

Séo Paulo é a maior cidade do Brasil em populagao.
Ga cote 12,50 € pour deux crépes et un thé glacé.
----- OUTPUT B -----
AEble, øl og smørrebrød er typisk dansk mad.
Bitte schließen Sie die Tür, bevor Sie gehen.
São Paulo é a maior cidade do Brasil em população.
Ça coûte 12,50 € pour deux crêpes et un thé glacé.


========== ITEM 092_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/092_mixed_styles.png
----- GROUND TRUTH -----
Weekly Summary
Read time: 4 min
Write the test first, watch it fail, then make it pass with the simplest code.
If the fan is loud, check which process is using the most CPU first.
He paid $42.50 for the cable, which was twice what it cost last year.
----- OUTPUT A -----
Weekly Summary

Read time: 4 min

Write the test first, watch it fail, then make it pass with the simplest code.
If the fan is loud, check which process is using the most CPU first.

He paid $42.50 for the cable, which was twice what it cost last year.
----- OUTPUT B -----
Weekly Summary
Read time: 4 min
Write the test first, watch it fail, then make it pass with the simplest code.
If the fan is loud, check which process is using the most CPU first.
He paid $42.50 for the cable, which was twice what it cost last year.


========== ITEM 096_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/096_mixed_styles.png
----- GROUND TRUTH -----
Account Overview
Updated 2 days ago
Do not store passwords in plain text; use a password manager instead.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
A tiling window manager arranges windows so that nothing ever overlaps.
----- OUTPUT A -----
Account Overview

Updated 2 days ago

Do not store passwords in plain text; use a password manager instead.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
A tiling window manager arranges windows so that nothing ever overlaps.
----- OUTPUT B -----
Account Overview
Updated 2 days ago
Do not store passwords in plain text; use a password manager instead.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
A tiling window manager arranges windows so that nothing ever overlaps.


========== ITEM 100_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/100_mixed_styles.png
----- GROUND TRUTH -----
Getting Started
Version 3.1 - October 2024
Rain is expected through the weekend, with temperatures around 14 degrees.
If the fan is loud, check which process is using the most CPU first.
Wayland compositors handle input, output and window management in one process.
----- OUTPUT A -----
Getting Started
Version 3.1 - October 2024

Rain is expected through the weekend, with temperatures around 14 degrees.
If the fan is loud, check which process is using the most CPU first.
Wayland compositors handle input, output and window management in one process.
----- OUTPUT B -----
Getting Started

Version 3.1 - October 2024

Rain is expected through the weekend, with temperatures around 14 degrees.
If the fan is loud, check which process is using the most CPU first.

‘Wayland compositors handle input, output and window management in one process.
