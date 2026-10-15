

========== ITEM 002_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/002_terminal.png
----- GROUND TRUTH -----
$ ping -c 3 archlinux.org
PING archlinux.org (95.217.163.246) 56(84) bytes of data.
64 bytes from 95.217.163.246: icmp_seq=1 ttl=52 time=38.4 ms
64 bytes from 95.217.163.246: icmp_seq=2 ttl=52 time=37.9 ms
--- archlinux.org ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
----- OUTPUT A -----
$ ping -c 3 archlinux.org
PING archlinux.org (95.217.163.246) 56(84) bytes of data.
64 bytes from 95.217.163.246: icmp_seq=1 ttl=52 time=38.4 ms
64 bytes from 95.217.163.246: icmp_seq=2 ttl=52 time=37.9 ms
    archlinux.org ping statistics
3 packets transmitted, 3 received, 0% packet loss
----- OUTPUT B -----
$ ping -c 3 archlinux.org

PING archlinux.org (95.217.163.246) 56(84) bytes of data.

64 bytes from 95.217.163.246: icmp_seq=1 ttl1=52 time=38.4 ms
64 bytes from 95.217.163.246: icmp_seq=2 ttl=52 time=37.9 ms
--- archlinux.org ping statistics ---

3 packets transmitted, 3 received, 0% packet loss


========== ITEM 006_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/006_terminal.png
----- GROUND TRUTH -----
$ git log --oneline -5
a3f9c21 Fix crash when monitor is unplugged
7b2e0d4 Add keybinding for OCR capture
e91c5aa Bump version to 3.1.2
4d8f6b3 Update README with install steps
0c7a1e9 Initial commit
----- OUTPUT A -----
  git log --oneline -5
a3f9c21 Fix crash when monitor is unplugged
7b2e0d4 Add keybinding for 0CR capture
e91c5aa Bump version to 3.1.2
4d8f6b3 Update README with install steps
0c7ale9 Initial commit
----- OUTPUT B -----
$ git log --oneline -5

a3£9c21 Fix crash when monitor is unplugged
7b2e0da Add keybinding for OCR capture
e91c5aa Bump version to 3.1.2

4d8feb3 Update README with install steps
6c7ale9 Initial commit


========== ITEM 010_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/010_terminal.png
----- GROUND TRUTH -----
$ systemctl status bluetooth
* bluetooth.service - Bluetooth service
     Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
     Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
   Main PID: 812 (bluetoothd)
----- OUTPUT A -----
$ systemctl status bluetooth
* bluetooth.service - Bluetooth service
Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
Main PID: 812 (bluetoothd)
----- OUTPUT B -----
$ systemctl status bluetooth
* bluetooth.service - Bluetooth service
     Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
     Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
   Main PID: 812 (bluetoothd)


========== ITEM 014_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/014_code.png
----- GROUND TRUTH -----
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop() if self._items else None
----- OUTPUT A -----
class Stack:
def __init_ (self):
self. items = []
def push(self, item):
self. _items.append(item)
def pop(self):
return self. _items.pop() if self._items else None
----- OUTPUT B -----
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop() if self._items else None


========== ITEM 018_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/018_code.png
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
func main() {
mn := map[string]int{"a": 1, "b": 2}
for k, v := range m {
fmt. Printf("%s=%d\n", k, v)
}
}


========== ITEM 022_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/022_prose.png
----- GROUND TRUTH -----
Backups are only useful if you have actually tried restoring from them.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
Compression trades CPU time for smaller files and faster transfers.
A tiling window manager arranges windows so that nothing ever overlaps.
The report covers Q3 revenue, hiring plans, and the new office in Berlin.
----- OUTPUT A -----
Backups are only useful if you have actually tried restoring from them.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
Compression trades CPU time for smaller files and faster transfers.
A tiling window manager arranges windows so that nothing ever overlaps.
The report covers Q3 revenue, hiring plans, and the new office in Berlin.
----- OUTPUT B -----
Backups are only useful if you have actually tried restoring from them.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.

Compression trades CPU time for smaller files and faster transfers.

A tiling window manager arranges windows so that nothing ever overlaps.
The report covers Q3 revenue, hiring plans, and the new office in Berlin.


========== ITEM 026_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/026_prose.png
----- GROUND TRUTH -----
Optical character recognition turns pixels back into text you can edit.
Do not store passwords in plain text; use a password manager instead.
Unplug the router, wait thirty seconds, and plug it back in again.
Wayland compositors handle input, output and window management in one process.
----- OUTPUT A -----
Optical character recognition turns pixels back into text you can edit.

Do not store passwords in plain text; use a password manager instead.

Unplug the router, wait thirty seconds, and plug it back in again.

‘Wayland compositors handle input, output and window management in one process.
----- OUTPUT B -----
Optical character recognition turns pixels back into text you can edit.
Do not store passwords in plain text; use a password manager instead.
Unplug the router, wait thirty seconds, and plug it back in again.
Wayland compositors handle input, output and window management in one process.


========== ITEM 030_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/030_ui.png
----- GROUND TRUTH -----
Wi-Fi Connected
HomeNetwork-5G Bluetooth
Off Airplane mode
----- OUTPUT A -----
   Wi-Fi   Connected
   HomeNetwork-5G   Bluetooth
  Off  Airplane mode
----- OUTPUT B -----
Wi-Fi                       Connected

HomeNetwork-5G             Bluetooth

Off                         Airplane mode


========== ITEM 034_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/034_ui.png
----- GROUND TRUTH -----
Settings Display Brightness Night Light Scale: 125% Apply Cancel
----- OUTPUT A -----
Settings     Display     Brightness     Night Light     Scale: 125%     Apply     Cancel
----- OUTPUT B -----
Settings   Display   Brightness   Night Light   Scale: 125%   Apply   Cancel


========== ITEM 038_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/038_ui.png
----- GROUND TRUTH -----
Share Copy link
Download Rename
Move to folder Delete
----- OUTPUT A -----

----- OUTPUT B -----
Share                      Copy link

Download                    Rename

Move to folder                Delete


========== ITEM 042_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/042_small_text.png
----- GROUND TRUTH -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Version 2.4.1 fixes the crash that occurred when resuming from suspend.
Do not store passwords in plain text; use a password manager instead.
The library closes at 9 PM on weekdays and at noon on Saturdays.
The museum's new wing displays maps drawn between 1650 and 1720.
----- OUTPUT A -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Version 2.4.1 fixes the crash that occurred when resuming from suspend.
Do not store passwords in plain text; use a password manager instead.
The library closes at 9 PM on weekdays and at noon on Saturdays.

The museum's new wing displays maps drawn between 1650 and 1720.
----- OUTPUT B -----
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Version 2.4.1 fixes the crash that occurred when resuming from suspend.
Do not store passwords in plain text; use a password manager instead.
The library closes at 9 PM on weekdays and at noon on Saturdays.
The museum's new wing displays maps drawn between 1650 and 1720.


========== ITEM 046_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/046_small_text.png
----- GROUND TRUTH -----
The quick brown fox jumps over the lazy dog near the riverbank.
Wayland compositors handle input, output and window management in one process.
Optical character recognition turns pixels back into text you can edit.
Screen readers depend on applications exposing correct accessibility labels.
The library closes at 9 PM on weekdays and at noon on Saturdays.
----- OUTPUT A -----
The ck brown ox amps over th lazy dog near th rverbank.

Wayland composiors handie nut, ouput and window management none proces.
Opal characte recogni pees Back no txt you can edt.

Screen readers depend on appcations expose cect acessibiy bes.

“Th rary closes a5 PM an eokdays and at oon on Saturdays.
----- OUTPUT B -----
The quick brown fox jumps over the lazy dog near the riverbank.
Wayland compositors handle input, output and window management in one process.
Optical character recognition turns pixels back into text you can edit.
Screen readers depend on applications exposing correct accessibility labels.
The library closes at 9 PM on weekdays and at noon on Saturdays.


========== ITEM 050_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/050_low_contrast.png
----- GROUND TRUTH -----
Unplug the router, wait thirty seconds, and plug it back in again.
Our support team replies within 24 hours, including weekends and holidays.
----- OUTPUT A -----
Unplug the router, wait thirty seconds, and plug it back in again.
Our support team replies within 24 hours, including weekends and holidays.
----- OUTPUT B -----
Unplug the router, wait thirty seconds, and plug it back in again.
Our support team replies within 24 hours, including weekends and holidays.


========== ITEM 054_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/054_low_contrast.png
----- GROUND TRUTH -----
The meeting moved to Thursday at 3:30 PM because the projector was broken.
Backups are only useful if you have actually tried restoring from them.
A tiling window manager arranges windows so that nothing ever overlaps.
----- OUTPUT A -----
The meeting moved to Thursday at 3:30 PM because the projector was broken.
Backups are only useful if you have actually tried restoring from them.
A tiling window manager arranges windows so that nothing ever overlaps.
----- OUTPUT B -----
The meeting moved to Thursday at 3:30 PM because the projector was broken.
Backups are only useful if you have actually tried restoring from them.
Atiling window manager arranges windows so that nothing ever overlaps.


========== ITEM 058_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/058_table.png
----- GROUND TRUTH -----
Key Action
Super + Return Terminal
Super + W Close window
Super + Space Launcher
Super + Ctrl + Print OCR
----- OUTPUT A -----
Key                Action
Super + Return       Terminal
Super + W           Close window
Super + Space       Launcher
Super + Ctrl + Print OCR
----- OUTPUT B -----
Key                  Action
Super + Return        Terminal
Super + W            Close window
Super + Space         Launcher
Super + Ctrl + Print OCR


========== ITEM 062_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/062_table.png
----- GROUND TRUTH -----
Station Arrives Departs Platform
Lyon 08:14 08:19 3
Dijon 09:47 09:52 1A
Paris 11:30 - 12
----- OUTPUT A -----
Station Arrives Departs Platform
Lyon   08:14 08:19   3
Dijon 09:47 09:52   1A
Paris 11:30          12
----- OUTPUT B -----
Station Arrives Departs Platform
Lyon     08:14     08:19     3

Dijon          09:47         09:52           1A

Paris         11:30        °                12


========== ITEM 066_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/066_identifiers.png
----- GROUND TRUTH -----
https://github.com/omega-lunar/river-7/pull/8579
omega.lunar43@example.com
UUID: 94d8dfb0-2470-7c17-5857-8f618aff0cea
Server: 150.15.100.234:3000
API_KEY=demo-a6e15XZ4aeQ712Y3Z154caYb
https://www.lunar-omega.org/docs/v1/getting-started?ref=nav#install
/home/user/.config/omega/lunar_17.toml
----- OUTPUT A -----
https://github.com/omega-lunar/river-7/pull/8579
omega.lunar43@example.com
UUID: 94d8dfb0-2470-7c17-5857-8f618aff0cea
Server：150.15.100.234:3000
API_KEY=demo-a6e15XZ4aeQ712Y3Z154caYb
https://www.lunar-omega.org/docs/v1/getting-started?ref=nav#install
/home/user/.config/omega/lunar_17.toml
----- OUTPUT B -----
https://github.com/omega- lunar/river-7/pull/8579

omega. lunar43@example.com

UUID: 94d8dfb0-2470-7c17-5857-8f618affOcea

Server: 150.15.100.234:3000

API_KEY=demo-a6el5XZ4aeQ712Y3Z154caYb

https://www. lunar-omega.org/docs/vl/getting-started?ref=nav#install
/home/user/.config/omega/lunar_17.toml


========== ITEM 070_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/070_identifiers.png
----- GROUND TRUTH -----
Server: 26.35.115.21:22
API_KEY=demo-3Z3ce17aZ428c8173266X8fc
commit e22c64b2d2d8926fa8cd76eca327835c28fbb543
/home/user/.config/delta/bravo_45.toml
UUID: 1cdcfa28-af25-6033-888b-f818b0f5334d
delta.bravo70@example.com
----- OUTPUT A -----
Server: 26.35.115.21:22
APl_KEY=demo-3Z3ce17aZ428c8173266X8fc
commit e22c64b2d2d8926fa8cd76eca327835c28fbb543
/home/user/.config/delta/bravo_45.toml
UUID: 1cdcfa28-af25-6033-888b-f818b0f5334d
delta.bravo70@example.com
----- OUTPUT B -----
Server: 26.35.115.21:22
API_KEY=demo-3Z3ce17aZ42808173266X8lc

‘commit 622064b2d2d8926faBod76ecad278350281bb543
/homeluser.config/deltarbravo_a5.toml

UUID: 1cdcfa28-af25-6033-888b-1818b0f5334d
delta.bravo70@example.com


========== ITEM 074_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/074_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2020-41757
Date: 09/11/2025
Amount due: $8,506.41
Phone: +1 (306) 795-4034
IBAN: DE75 2318 5550 9848 3891 37
Version 1.6.55 (build 89728)
----- OUTPUT A -----
Invoice No. INV-2020-41757

Date: 09/11/2025

Amount due: $8,506.41

Phone: +1 (306) 795-4034

IBAN: DE75 2318 5550 9848 3891 37
Version 1.6.55 (build 89728)
----- OUTPUT B -----
Invoice No. INV-2020-41757
Date:09/11/2025
Amount due: $8,506.41
Phone: +1 (306) 795-4034
IBAN: DE75 2318 5550 9848 3891 37
Version 1.6.55 (build 89728)


========== ITEM 078_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/078_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2022-05102
Date: 25/08/2021
Amount due: $4,562.38
Phone: +1 (686) 637-4811
IBAN: DE71 1918 6952 2376 9202 57
----- OUTPUT A -----
Invoice No. INV-2022-05102
Date：25/08/2021
Amount due: $4,562.38
Phone: +1 (686) 637-4811
IBAN: DE71 1918 6952 2376 9202 57
----- OUTPUT B -----
Invoice No. INV-2022-05102

Date: 25/08/2021

Amount due: $4,562.38

Phone: +1 (686) 637-4811

IBAN: DE71 1918 6952 2376 9202 57


========== ITEM 082_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/082_accented.png
----- GROUND TRUTH -----
Über den Wolken muss die Freiheit wohl grenzenlos sein.
Señor Núñez llegó tarde a la estación de tren.
El niño comió una manzana mientras leía el periódico.
Die Größe der Datei überschreitet das zulässige Maximum.
----- OUTPUT A -----
Über den Wolken muss die Freiheit wohl grenzenlos sein.
Señor Núñez llegó tarde a la estación de tren.
El niño comió una manzana mientras leía el periódico.
Die Größe der Datei überschreitet das zulässige Maximum.
----- OUTPUT B -----
Uber den Wolken muss die Freiheit wohl grenzenlos sein.
Sefior Nufiez llegé tarde a la estacion de tren.

El nifio comié una manzana mientras leia el periédico.

Die GroBe der Datei lberschreitet das zulassige Maximum.


========== ITEM 086_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/086_accented.png
----- GROUND TRUTH -----
La reunión será el miércoles a las diez de la mañana.
Ça coûte 12,50 € pour deux crêpes et un thé glacé.
Le café de la gare est fermé le dimanche après-midi.
Bitte schließen Sie die Tür, bevor Sie gehen.
----- OUTPUT A -----
La reuni6n seré el miércoles a las diez de la mafiana.
Ga cote 12,50 € pour deux crépes et un thé glacé.
Le café de la gare est fermé le dimanche aprés-midi.
Bitte schlieBen Sie die Tur, bevor Sie gehen.
----- OUTPUT B -----
La reunión será el miércoles a las diez de la mañana.
ça coûte 12,50 € pour deux crêpes et un thé glacé.
Le café de la gare est fermé le dimanche après-midi.
Bitte schließen Sie die Tür, bevor Sie gehen.


========== ITEM 090_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/090_mixed_styles.png
----- GROUND TRUTH -----
Troubleshooting
Read time: 4 min
The museum's new wing displays maps drawn between 1650 and 1720.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
She opened the terminal, typed a single command, and the build finally passed.
----- OUTPUT A -----
Troubleshooting

The museum's new wing displays maps drawn between 1650 and 1720.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.

She opened the terminal, typed a single command, and the build finally passed.
----- OUTPUT B -----
Troubleshooting
Read time: 4 min
The museum's new wing displays maps drawn between 1650 and 1720.
The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.
She opened the terminal, typed a single command, and the build finally passed.


========== ITEM 094_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/094_mixed_styles.png
----- GROUND TRUTH -----
Release Notes
Updated 2 days ago
The meeting moved to Thursday at 3:30 PM because the projector was broken.
The report covers Q3 revenue, hiring plans, and the new office in Berlin.
Version 2.4.1 fixes the crash that occurred when resuming from suspend.
----- OUTPUT A -----
Release Notes

Updated 2 days ago

The meeting moved to Thursday at 3:30 PM because the projector was broken.
The report covers Q3 revenue, hiring plans, and the new office in Berlin.

Version 2.4.1 fixes the crash that occurred when resuming from suspend.
----- OUTPUT B -----
Release Notes
Updated 2 days ago
The meeting moved to Thursday at 3:30 PM because the projector was broken.
The report covers Q3 revenue, hiring plans, and the new office in Berlin.
Version 2.4.1 fixes the crash that occurred when resuming from suspend.


========== ITEM 098_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/098_mixed_styles.png
----- GROUND TRUTH -----
Weekly Summary
Last synced 10:42
Readable code is written for the next person, who is usually you.
If the fan is loud, check which process is using the most CPU first.
The meeting moved to Thursday at 3:30 PM because the projector was broken.
----- OUTPUT A -----
Weekly Summary
Last synced 10:42
Readable code is written for the next person, who is usually you.
If the fan is loud, check which process is using the most CPU first.
The meeting moved to Thursday at 3:30 PM because the projector was broken.
----- OUTPUT B -----
Weekly Summary

Last synced 10:42

Readable code is written for the next person, who is usually you.

If the fan is loud, check which process is using the most CPU first.

The meeting moved to Thursday at 3:30 PM because the projector was broken.
