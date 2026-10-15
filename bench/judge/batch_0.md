

========== ITEM 001_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/001_terminal.png
----- GROUND TRUTH -----
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            15Gi       8.3Gi       758Mi       806Mi       8.0Gi       7.0Gi
Swap:          4.0Gi       512Mi       3.5Gi
----- OUTPUT A -----
$ free -h

total        used        free      shared buff/cache   available
Mem:            15Gi       8.3Gi       758Mi       806Mi       8.061       7.061
Swap:          4.0G1i       512Mi       3.561
----- OUTPUT B -----
$ free -h
              total       used       free     shared buff/cache available
Mem:          15Gi      8.3Gi      758Mi      806Mi      8.0Gi      7.0Gi
Swap:         4.0Gi      512Mi      3.5Gi


========== ITEM 005_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/005_terminal.png
----- GROUND TRUTH -----
$ docker ps
CONTAINER ID   IMAGE           STATUS          PORTS
5f2a9c1e7b3d   postgres:16     Up 2 hours      0.0.0.0:5432->5432/tcp
b81d04e6a2f9   redis:7-alpine  Up 2 hours      6379/tcp
----- OUTPUT A -----
$ docker ps

CONTAINER ID   IMAGE           STATUS          PORTS

5f2a9cle7b3d   postgres:16     Up 2 hours      0.0.0.0:5432->5432/tcp
b81d04e6a2f9  redis:7-alpine Up 2 hours      6379/tcp
----- OUTPUT B -----
$ docker ps
CONTAINER ID IMAGE          STATUS         PORTS
5f2a9c1e7b3d postgres:16    Up 2 hours     0.0.0.0:5432->5432/tcp
b81d04e6a2f9 redis:7-alpine Up 2 hours     6379/tcp


========== ITEM 009_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/009_terminal.png
----- GROUND TRUTH -----
$ systemctl status bluetooth
* bluetooth.service - Bluetooth service
     Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
     Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
   Main PID: 812 (bluetoothd)
----- OUTPUT A -----
S systemctl status bluetooth
 bluetooth.service - Bluetooth service
     Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
     Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
   Main PID: 812 (bluetoothd)
----- OUTPUT B -----
$ systemctl status bluetooth
* bluetooth.service - Bluetooth service
Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
Main PID: 812 (bluetoothd)


========== ITEM 013_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/013_code.png
----- GROUND TRUTH -----
const fetchUser = async (id) => {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};
----- OUTPUT A -----
const fetchUser = async (id) => {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};
----- OUTPUT B -----
const fetchUser = async (id) => {
const res = await fetch('/api/users/${id}");
if (!res.ok) throw new Error( HTTP ${res.status}");
return res.json();

Yi


========== ITEM 017_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/017_code.png
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
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop() if self._items else None
----- OUTPUT B -----
class Stack:
def __init__ (self):
self. items = []
def push(self, item):
self._items.append (item)
def pop(self):
return self. items.pop() if self. items else None


========== ITEM 021_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/021_prose.png
----- GROUND TRUTH -----
The archive contains 1,284 photos taken between 2019 and 2024.
Small, frequent commits make it far easier to find the change that broke things.
Unplug the router, wait thirty seconds, and plug it back in again.
Our support team replies within 24 hours, including weekends and holidays.
Most performance problems come from doing work that never needed to happen.
Write the test first, watch it fail, then make it pass with the simplest code.
----- OUTPUT A -----
The archive contains 1,284 photos taken between 2019 and 2024.

Small, frequent commits make it far easier to find the change that broke things.
Unplug the router, wait thirty seconds, and plug it back in again.

Our support team replies within 24 hours, including weekends and holidays.
Most performance problems come from doing work that never needed to happen.
Write the test first, watch it fail, then make it pass with the simplest code.
----- OUTPUT B -----
The archive contains 1,284 photos taken between 2019 and 2024.
Small, frequent commits make it far easier to find the change that broke things.
Unplug the router, wait thirty seconds, and plug it back in again.
Our support team replies within 24 hours, including weekends and holidays.
Most performance problems come from doing work that never needed to happen.
Write the test first, watch it fail, then make it pass with the simplest code.


========== ITEM 025_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/025_prose.png
----- GROUND TRUTH -----
The quick brown fox jumps over the lazy dog near the riverbank.
Most performance problems come from doing work that never needed to happen.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
Compression trades CPU time for smaller files and faster transfers.
----- OUTPUT A -----
The quick brown fox jumps over the lazy dog near the riverbank.

Most performance problems come from doing work that never needed to happen.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
Compression trades CPU time for smaller files and faster transfers.
----- OUTPUT B -----
The quick brown fox jumps over the lazy dog near the riverbank.
Most performance problems come from doing work that never needed to happen.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
Compression trades CPU time for smaller files and faster transfers.


========== ITEM 029_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/029_ui.png
----- GROUND TRUTH -----
Downloads Documents Pictures Music Videos Trash
----- OUTPUT A -----
Downloads ~~ Documents Pictures Music Videos Trash
----- OUTPUT B -----
Downloads Documents Pictures Music Videos Trash


========== ITEM 033_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/033_ui.png
----- GROUND TRUTH -----
Downloads Documents Pictures Music Videos Trash
----- OUTPUT A -----
Downloads Documents Pictures Music Videos Trash
----- OUTPUT B -----
Downloads   Documents   Pictures   Music   Videos   Trash


========== ITEM 037_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/037_ui.png
----- GROUND TRUTH -----
Wi-Fi
Connected
HomeNetwork-5G
Bluetooth
Off
Airplane mode
----- OUTPUT A -----
Wi-Fi
HomeNetwork-5G
Bluetooth

Off

Airplane mode
----- OUTPUT B -----
Wi-Fi

Connected

HomeNetwork-5G

Bluetooth

Off

Airplane mode


========== ITEM 041_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/041_small_text.png
----- GROUND TRUTH -----
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
Good error messages explain what happened, why, and what to do next.
Write the test first, watch it fail, then make it pass with the simplest code.
If the fan is loud, check which process is using the most CPU first.
----- OUTPUT A -----
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.

Good error messages explain what happened, why, and what to do next.

Write the test first, watch it fail, then make it pass with the simplest code.
If the fan is loud, check which process is using the most CPU first.
----- OUTPUT B -----
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
Backups are only useful if you have actually tried restoring from them.
Good error messages explain what happened, why, and what to do next.
Write the test first, watch it fail, then make it pass with the simplest code.
If the fan is loud, check which process is using the most CPU first.


========== ITEM 045_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/045_small_text.png
----- GROUND TRUTH -----
Most performance problems come from doing work that never needed to happen.
The museum's new wing displays maps drawn between 1650 and 1720.
She opened the terminal, typed a single command, and the build finally passed.
Do not store passwords in plain text; use a password manager instead.
----- OUTPUT A -----
Most performance problems come from doing work that never needed to happen.
The museum's new wing displays maps drawn between 1650 and 1720.
She opened the terminal, typed a single command, and the build finally passed.
Do not store passwords in plain text; use a password manager instead.
----- OUTPUT B -----
Most performance problems come from doing work that never needed to happen.
“The museum's new wing displays maps drawn between 1650 and 1720.

She opened the terminal typed a single command, and the build finally passed.
Do not store passwords in plain text; use a password manager instead


========== ITEM 049_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/049_low_contrast.png
----- GROUND TRUTH -----
He paid $42.50 for the cable, which was twice what it cost last year.
Good error messages explain what happened, why, and what to do next.
Our support team replies within 24 hours, including weekends and holidays.
----- OUTPUT A -----
He paid $42.50 for the cable, which was twice what it cost last year.
Good error messages explain what happened, why, and what to do next.
Our support team replies within 24 hours, including weekends and holidays.
----- OUTPUT B -----
He paid $42.50 for the cable, which was twice what it cost last year.
Good error messages explain what happened, why, and what to do next.
Our support team replies within 24 hours, including weekends and holidays.


========== ITEM 053_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/053_low_contrast.png
----- GROUND TRUTH -----
The report covers Q3 revenue, hiring plans, and the new office in Berlin.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Write the test first, watch it fail, then make it pass with the simplest code.
Rain is expected through the weekend, with temperatures around 14 degrees.
----- OUTPUT A -----
The report covers Q3 revenue, hiring plans, and the new office in Berlin.

Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.

Write the test first, watch it fail, then make it pass with the simplest code.

Rain is expected through the weekend, with temperatures around 14 degrees.
----- OUTPUT B -----
The report covers Q3 revenue, hiring plans, and the new office in Berlin.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
Write the test first, watch it fail, then make it pass with the simplest code.
Rain is expected through the weekend, with temperatures around 14 degrees.


========== ITEM 057_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/057_table.png
----- GROUND TRUTH -----
Station Arrives Departs Platform
Lyon 08:14 08:19 3
Dijon 09:47 09:52 1A
Paris 11:30 - 12
----- OUTPUT A -----
Station Arrives Departs Platform
Lyon          08:14        08:19        El

Dijon      09:47      09:52      1A

Paris      11:30      -           12
----- OUTPUT B -----
Station Arrives Departs Platform
Lyon   08:14 08:19 3
Dijon 09:47 09:52 1A
Paris 11:30          12


========== ITEM 061_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/061_table.png
----- GROUND TRUTH -----
PID USER CPU% MEM% COMMAND
1043 user 12.4 3.1 chromium
877 root 4.0 0.8 Hyprland
2210 user 1.7 1.2 alacritty
15 root 0.0 0.0 kthreadd
----- OUTPUT A -----
PID USER CPUS MEN% COMMAND

1043 user 12.4 3.1 chromium
877 root 4.0 0.8 Hyprland
2210 user 1.7 1.2  alacritty
15 root 0.0 0.0 kthreadd
----- OUTPUT B -----
PID USER CPU% MEM% COMMAND
1043 user 12.4 3.1 chromium
877 root 4.0 0.8 Hyprland
2210 user 1.7 1.2 alacritty
15 root 0.0 0.0 kthreadd


========== ITEM 065_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/065_identifiers.png
----- GROUND TRUTH -----
commit 0043b68b8c45807d902fd7bda7a6257a33d245a1
Server: 51.63.105.190:3000
API_KEY=demo-7Qab97fa212de20X3Yb5eYed
UUID: adcbf2f8-3fab-17ed-3323-6fcea7a92af7
----- OUTPUT A -----
‘commit 0043b6808c458070902107bda7a6257a33d245a1
Server: 51.63.105.190:3000
API_KEY=demo-7Qab97fa212de20X3YbSeYed

UUID: adchi2fa-3fab-17ed-3323-6icea7a02afl
----- OUTPUT B -----
commit 0043b68b8c45807d902fd7bda7a6257a33d245a1
Server: 51.63.105.190:3000
API_KEY=demo-7Qab97fa212de20X3Yb5eYed
UUID: adcbf2f8-3fab-17ed-3323-6fcea7a92af7


========== ITEM 069_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/069_identifiers.png
----- GROUND TRUTH -----
/home/user/.config/river/cloud_10.toml
API_KEY=demo-f2cc61bX96Qd5Z98Y050b917
Server: 196.177.144.207:8080
https://github.com/river-cloud/omega-5/pull/3916
UUID: a845c12e-5895-5392-9587-bfe0796a38a0
river.cloud69@example.com
https://www.cloud-river.org/docs/v4/getting-started?ref=nav#install
----- OUTPUT A -----
/home/user/.config/river/cloud_10.toml
API_KEY=demo-f2cc610X96Qd5298Y050b917

Server: 196.177.144.207:8080
https://github.com/river-cloud/omega-5/pull/3916

UUID: a845c12e-5895-5392-9587-bfe0796a38a0
river.cloudé9@example.com
https://www.cloud-river.org/docs/v4/getting-started?ref=nav#install
----- OUTPUT B -----
/home/user/.config/river/cloud_10.toml
API_KEY=demo-f2cc61bX96Qd5Z98Y050b917
Server: 196.177.144.207:8080
https://github.com/river-cloud/omega-5/pull/3916
UUID: a845c12e-5895-5392-9587-bfe0796a38a0
river.cloud69@example.com
https://www.cloud-river.org/docs/v4/getting-started?ref=nav#install


========== ITEM 073_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/073_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2023-04114
Date: 06/10/2025
Amount due: $1,934.60
Phone: +1 (809) 775-1181
IBAN: DE32 9968 6182 8249 5213 85
----- OUTPUT A -----
Invoice No. INV-2023-04114

Date: 06/10/2025

Amount due: $1,934.60

Phone: +1 (809) 775-1181

IBAN: DE32 9968 6182 8249 5213 85
----- OUTPUT B -----
Invoice No. INV-2023-04114
Date: 06/10/2025
Amount due: $1,934.60
Phone: +1 (809) 775-1181
IBAN: DE32 9968 6182 8249 5213 85


========== ITEM 077_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/077_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2025-73375
Date: 26/10/2023
Amount due: $2,059.75
Phone: +1 (471) 430-8108
----- OUTPUT A -----
Invoice No. INV-2025-73375
Date: 26/10/2023

Amount due: $2,059.75
Phone: +1 (471) 430-8108
----- OUTPUT B -----
Invoice No. INV-2025-73375
Date: 26/10/2023
Amount due: $2,059.75
Phone: +1 (471) 430-8108


========== ITEM 081_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/081_accented.png
----- GROUND TRUTH -----
Ça coûte 12,50 € pour deux crêpes et un thé glacé.
Le café de la gare est fermé le dimanche après-midi.
Où est la bibliothèque la plus proche, s'il vous plaît ?
Bitte schließen Sie die Tür, bevor Sie gehen.
Je préfère le thé à la menthe après le dîner.
----- OUTPUT A -----
Ca colte 12,50 € pour deux crépes et un thé glacé.
Le café de la gare est fermé le dimanche aprés-midi.
Ou est la bibliotheque la plus proche, s'il vous plait ?
Bitte schliefen Sie die Tur, bevor Sie gehen.

Je préfere le thé a la menthe apres le diner.
----- OUTPUT B -----
Ça coûte 12,50 € pour deux crêpes et un thé glacé.
Le café de la gare est fermé le dimanche après-midi.
Où est la bibliothèque la plus proche, s'il vous plaît ?
Bitte schließen Sie die Tür, bevor Sie gehen.
Je préfère le thé à la menthe après le dîner.


========== ITEM 085_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/085_accented.png
----- GROUND TRUTH -----
Æble, øl og smørrebrød er typisk dansk mad.
Die Größe der Datei überschreitet das zulässige Maximum.
Ça coûte 12,50 € pour deux crêpes et un thé glacé.
----- OUTPUT A -----
/Eble, ol 0g smorrebrod er typisk dansk mad.
Die GroRe der Datei liberschreitet das zulassige Maximum
Ca colite 12,50 € pour deux crépes et un thé glacé.
----- OUTPUT B -----
AEble, øl og smørrebrød er typisk dansk mad.
Die Größe der Datei überschreitet das zulässige Maximum.
Ça coûte 12,50 € pour deux crêpes et un thé glacé.


========== ITEM 089_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/089_mixed_styles.png
----- GROUND TRUTH -----
Troubleshooting
Read time: 4 min
Unplug the router, wait thirty seconds, and plug it back in again.
Small, frequent commits make it far easier to find the change that broke things.
Readable code is written for the next person, who is usually you.
----- OUTPUT A -----
Troubleshooting
Read time: 4 min
Unplug the router, wait thirty seconds, and plug it back in again.
Small, frequent commits make it far easier to find the change that broke things.
Readable code is written for the next person, who is usually you.
----- OUTPUT B -----
Troubleshooting

Read time: 4 min

Unplug the router, wait thirty seconds, and plug it back in again.

Small, frequent commits make it far easier to find the change that broke things.
Readable code is written for the next person, who is usually you.


========== ITEM 093_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/093_mixed_styles.png
----- GROUND TRUTH -----
Getting Started
Updated 2 days ago
The archive contains 1,284 photos taken between 2019 and 2024.
If the fan is loud, check which process is using the most CPU first.
Unplug the router, wait thirty seconds, and plug it back in again.
----- OUTPUT A -----
Getting Started

The archive contains 1,284 photos taken between 2019 and 2024.
If the fan is loud, check which process is using the most CPU first.
Unplug the router, wait thirty seconds, and plug it back in again.
----- OUTPUT B -----
Getting Started
Updated 2 days ago
The archive contains 1,284 photos taken between 2019 and 2024.
If the fan is loud, check which process is using the most CPU first.
Unplug the router, wait thirty seconds, and plug it back in again.


========== ITEM 097_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/097_mixed_styles.png
----- GROUND TRUTH -----
Weekly Summary
Updated 2 days ago
Our support team replies within 24 hours, including weekends and holidays.
Do not store passwords in plain text; use a password manager instead.
The meeting moved to Thursday at 3:30 PM because the projector was broken.
----- OUTPUT A -----
Weekly Summary

Our support team replies within 24 hours, including weekends and holidays.
Do not store passwords in plain text; use a password manager instead.

The meeting moved to Thursday at 3:30 PM because the projector was broken.
----- OUTPUT B -----
Weekly Summary
Updated 2 days ago
Our support team replies within 24 hours, including weekends and holidays.
Do not store passwords in plain text; use a password manager instead.
The meeting moved to Thursday at 3:30 PM because the projector was broken.
