

========== ITEM 003_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/003_terminal.png
----- GROUND TRUTH -----
error[E0382]: borrow of moved value: `config`
  --> src/main.rs:14:20
   |
12 |     let handle = spawn(config);
   |                        ------ value moved here
14 |     println!("{:?}", config);
   |                      ^^^^^^ value borrowed here after move
----- OUTPUT A -----
error[E0382]: borrow of moved value: “config’
--> src/main.rs:14:20
|
12 |    let handle = spawn(config);
|                   ------ value moved here
14 |    println! ("{:?}", config);
|                  ANAAAA value borrowed here after move
----- OUTPUT B -----
error[E0382]: borrow of moved value: `config
  --> src/main.rs:14:20

12      let handle = spawn(config);
                                  value moved here
14      println!("{:?}", config);
                         ^ value borrowed here after move


========== ITEM 007_terminal ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/007_terminal.png
----- GROUND TRUTH -----
$ curl -s https://api.github.com/repos/basecamp/omarchy | jq .stargazers_count
18342
----- OUTPUT A -----
$ curl -s https://api.github.com/repos/basecamp/omarchy | jq .stargazers_count
18342
----- OUTPUT B -----
$ curl -s https://api.github.com/repos/basecamp/omarchy I jq .stargazers_count
18342


========== ITEM 011_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/011_code.png
----- GROUND TRUTH -----
def parse_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "version" not in data:
        raise ValueError(f"missing version in {path}")
    return {k: v for k, v in data.items() if v is not None}
----- OUTPUT A -----
def parse_config(path: str) -> dict:
with open(path, "r*, encoding="utf-8") as f:
data = json.load(f)
if “version” not in data:
raise ValueError(f'missing version in {path}")
return {k: v for k, v in data.items() if v is not None}
----- OUTPUT B -----
def parse_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.1oad(f)
    if "version" not in data:
        raise ValueError(f"missing version in {path}")
    return {k: v for k, v in data.items() if v is not None}


========== ITEM 015_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/015_code.png
----- GROUND TRUTH -----
fn main() {
    let nums: Vec<i32> = (1..=10).collect();
    let sum: i32 = nums.iter().filter(|&x| x % 2 == 0).sum();
    println!("sum of evens = {}", sum);
}
----- OUTPUT A -----
fn main() {
    let nums: Vec<i32> = (1..=10).collect();
    let sum: i32 = nums.iter().filter(l&x| x % 2 == 0).sum();
    println!("sum of evens = {}", sum);
}
----- OUTPUT B -----
fn main) {
let nums: Vec<i32> = (1..=10).collect();
let sum: i32 = nums.iter().filter(|&x| x % 2 == 0).sum();
println! ("sum of evens = {}", sum);

is


========== ITEM 019_code ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/019_code.png
----- GROUND TRUTH -----
for (int i = 0; i < n; ++i) {
    if (arr[i] < 0 && i != last) {
        arr[i] = -arr[i] * 2;
    }
}
printf("%d items, max=%.2f\n", n, max);
----- OUTPUT A -----
for (int i= 0; i <n; ++i) {
if (arr[i] < 0 && i != last) {
arr[i] = -arr[i] * 2;
bh
}
printf("%d items, max=¥.2f\n", n, max);
----- OUTPUT B -----
for (int i = 0; i < n; ++i) {
    if (arr[i] < 0 && i != last) {
        arr[i] = -arr[i] * 2;
    }
}
printf("%d items, max=%.2f\n", n, max);


========== ITEM 023_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/023_prose.png
----- GROUND TRUTH -----
Unplug the router, wait thirty seconds, and plug it back in again.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
She opened the terminal, typed a single command, and the build finally passed.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
----- OUTPUT A -----
Unplug the router, wait thirty seconds, and plug it back in again.
Every keyboard shortcut you learn saves a few seconds a hundred times a day.
She opened the terminal, typed a single command, and the build finally passed.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
----- OUTPUT B -----
Unplug the router, wait thirty seconds, and plug it back in again.

Every keyboard shortcut you learn saves a few seconds a hundred times a day.
She opened the terminal, typed a single command, and the build finally passed.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.


========== ITEM 027_prose ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/027_prose.png
----- GROUND TRUTH -----
Readable code is written for the next person, who is usually you.
Rain is expected through the weekend, with temperatures around 14 degrees.
The library closes at 9 PM on weekdays and at noon on Saturdays.
----- OUTPUT A -----
Readable code is written for the next person, who is usually you.
Rain is expected through the weekend, with temperatures around 14 degrees.
The library closes at 9 PM on weekdays and at noon on Saturdays.
----- OUTPUT B -----
Readable code is written for the next person, who is usually you.
Rain is expected through the weekend, with temperatures around 14 degrees.
The library closes at 9 PM on weekdays and at noon on Saturdays.


========== ITEM 031_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/031_ui.png
----- GROUND TRUTH -----
Downloads Documents
Pictures Music
Videos Trash
----- OUTPUT A -----
Downloads                  Documents

Pictures                    Music

Videos                      Trash
----- OUTPUT B -----



========== ITEM 035_ui ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/035_ui.png
----- GROUND TRUTH -----
Battery 87% Power Saver Balanced Performance 2:41 remaining
----- OUTPUT A -----
Battery 87%     Power Saver     Balanced     Performance     2:41 remaining
----- OUTPUT B -----
Battery 87%   Power Saver   Balanced   Performance   2:41 remaining


========== ITEM 039_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/039_small_text.png
----- GROUND TRUTH -----
The quick brown fox jumps over the lazy dog near the riverbank.
Do not store passwords in plain text; use a password manager instead.
The library closes at 9 PM on weekdays and at noon on Saturdays.
The archive contains 1,284 photos taken between 2019 and 2024.
----- OUTPUT A -----
The quick brown fox jumps over the lazy dog near the riverbank.
Do not store passwords in plain text; use a password manager instead.
The library closes at 9 PM on weekdays and at noon on Saturdays.
The archive contains 1,284 photos taken between 2019 and 2024.
----- OUTPUT B -----
The quick brown fox jumps over the lazy dog near the riverbank.

Do not store passwords in plain text; use a password manager instead.
The Library closes at © PM on weekdays and at noon on Saturdays.

The archive contains 1,284 photos taken between 2019 and 2024.


========== ITEM 043_small_text ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/043_small_text.png
----- GROUND TRUTH -----
Most performance problems come from doing work that never needed to happen.
Keep your dotfiles in version control so a new machine takes minutes, not days.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
----- OUTPUT A -----
Most performance problems come from doing work that never needed to happen.
Keep your doffiles in version control so a new machine takes minutes, not days.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.
----- OUTPUT B -----
Most performance problems come from doing work that never needed to happen.
Keep your dotfiles in version control so a new machine takes minutes, not days.
Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.


========== ITEM 047_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/047_low_contrast.png
----- GROUND TRUTH -----
If the fan is loud, check which process is using the most CPU first.
Rain is expected through the weekend, with temperatures around 14 degrees.
Write the test first, watch it fail, then make it pass with the simplest code.
The archive contains 1,284 photos taken between 2019 and 2024.
----- OUTPUT A -----
If the fan is loud, check which process is using the most CPU first.
Rain is expected through the weekend, with temperatures around 14 degrees.
Write the test first, watch it fail, then make it pass with the simplest code.
The archive contains 1,284 photos taken between 2019 and 2024.
----- OUTPUT B -----
If the fan is loud, check which process is using the most CPU first.

Rain is expected through the weekend, with temperatures around 14 degrees.
Write the test first, watch it fail, then make it pass with the simplest code.
The archive contains 1,284 photos taken between 2019 and 2024.


========== ITEM 051_low_contrast ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/051_low_contrast.png
----- GROUND TRUTH -----
Compression trades CPU time for smaller files and faster transfers.
Most performance problems come from doing work that never needed to happen.
----- OUTPUT A -----
Compression trades CPU time for smaller files and faster transfers.
Most performance problems come from doing work that never needed to happen.
----- OUTPUT B -----
Compression trades CPU time for smaller files and faster transfers.
Most performance problems come from doing work that never needed to happen.


========== ITEM 055_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/055_table.png
----- GROUND TRUTH -----
Month Revenue Costs Profit
Jan 12,430 9,210 3,220
Feb 13,980 9,875 4,105
Mar 15,102 10,640 4,462
Apr 14,377 10,021 4,356
----- OUTPUT A -----
Month Revenue Costs Profit
Jan       12,430      9,210    3,220
Feb       13,980      9,875     4,105
Mar       15,102      10,640 4,462
Apr      14,377      10,021 4,356
----- OUTPUT B -----
Month Revenue Costs Profit
Jan    12,430   9,210 3,220
Feb    13,980   9,875 4,105
Mar   15,102   10,640 4,462
Apr    14,377   10,021 4,356


========== ITEM 059_table ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/059_table.png
----- GROUND TRUTH -----
Package Old New
linux 6.10.9 6.11.3
mesa 24.2.3 24.2.4
hyprland 0.44.0 0.44.1
firefox 130.0.1 131.0
----- OUTPUT A -----
Package Old              New

linux        6.10.9     6.11.3
mesa      2423    2424
hyprland ~~ 0.440 0.44.1
firefox         130.01 131.0
----- OUTPUT B -----
Package Old     New
linux      6.10.9   6.11.3
mesa     24.2.3   24.2.4
hyprland   0.44.0   0.44.1
firefox    130.0.1 131.0


========== ITEM 063_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/063_identifiers.png
----- GROUND TRUTH -----
cloud.bravo74@example.com
Server: 80.18.162.9:5432
/home/user/.config/cloud/bravo_38.toml
API_KEY=demo-d31047Z0bYfXQ162XaX4aYY8
----- OUTPUT A -----
cloud.bravo74@example.com
Server:80.18.162.9:5432
/home/user/.config/cloud/bravo_38.toml
API_KEY=demo-d31047Z0bYfXQ162XaX4aYY8
----- OUTPUT B -----
cloud.bravo74@example.com

Server: 80.18.162.9:5432
/home/user/.config/cloud/bravo_38.toml
API_KEY=demo-d31047Z0bYfXQ162XaX4aYY8


========== ITEM 067_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/067_identifiers.png
----- GROUND TRUTH -----
https://www.alpha-stone.org/docs/v1/getting-started?ref=nav#install
Server: 181.91.68.217:443
API_KEY=demo-9478962ZY2916d3Qc1Xc4e15
https://github.com/stone-alpha/pixel-5/pull/1197
/home/user/.config/stone/alpha_17.toml
stone.alpha85@example.com
----- OUTPUT A -----
https://www.alpha-stone.org/docs/v1/getting-started?ref=nav#install
Server:181.91.68.217:443
API_KEY=demo-9478962ZY2916d3Qc1Xc4e15
https://github.com/stone-alpha/pixel-5/pull/1197
/home/user/.config/stone/alpha_17.toml
stone.alpha85@example.com
----- OUTPUT B -----
https://www.alpha-stone.org/docs/vl/getting-started?ref=nav#install
Server: 181.91.68.217:443

API_KEY=demo-9478962ZY2916d3Qc1Xc4el5
https://github.com/stone-alpha/pixel-5/pull/1197
/home/user/.config/stone/alpha_17.toml

stone.alpha85@example.com


========== ITEM 071_identifiers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/071_identifiers.png
----- GROUND TRUTH -----
Server: 157.232.235.68:8080
UUID: fe08eda2-b3f2-13bb-8b18-542383f8e3eb
commit 1d1471ea13c467001f0d62ae13c4a57a5a9aadd3
API_KEY=demo-QcYZ9QbX1a016QY8Y04a4Xa8
/home/user/.config/alpha/river_22.toml
https://github.com/alpha-river/stone-4/pull/8385
https://www.river-alpha.org/docs/v2/getting-started?ref=nav#install
----- OUTPUT A -----
Server: 157.232.235.68:8080

UUID: fe@8eda2-b3£2-13bb-8b18-54238318e3eb

commit 1d1471ea13c467001£0d62ae13c4a57a5a9aadd3
API_KEY=demo-QcYZ90bX1a016QY8Y04alXa8

/home /usex/.config/alpha/Tiver_22.toml

https: //github.com/alpha-river/stone-4/pull/8385

https: //www. river-alpha.oxrg/docs/v2/getting-started?ref=nav#install
----- OUTPUT B -----
Server:157.232.235.68:8080
UUID: fe08eda2-b3f2-13bb-8b18-542383f8e3eb
commit 1d1471ea13c467001f0d62ae13c4a57a5a9aadd3
API_KEY=demo-QcYZ9QbX1a016QY8Y04a4Xa8
/home/user/.config/alpha/river_22.toml
https://github.com/alpha-river/stone-4/pull/8385
https://www.river-alpha.org/docs/v2/getting-started?ref=nav#install


========== ITEM 075_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/075_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2025-34008
Date: 25/06/2022
Amount due: $1,861.06
Phone: +1 (482) 253-5801
IBAN: DE85 5844 7148 5219 1727 19
Version 7.3.98 (build 21244)
Order total: 72 items, 8.33 kg
Tracking: 1ZF5M5X860J8DLJ8VE
----- OUTPUT A -----
Invoice No. INV-2025-34008
Date: 25/06/2022
Amount due: $1,861.06
Phone: +1 (482) 253-5801
IBAN: DE85 5844 7148 5219 1727 19
Version 7.3.98 (build 21244)
Order total: 72 items, 8.33 kg
Tracking: 1ZF5M5X860J8DLJ8VE
----- OUTPUT B -----
Invoice No. INV-2025-34008

Date: 25/06/2022

Amount due: $1,861.06

Phone: +1 (482) 253-5801

IBAN: DE85 5844 7148 5219 1727 19
Version 7.3.98 (build 21244)

Order total: 72 items, 8.33 kg.
Tracking: 1ZF5M5X860J8DLJ8VE


========== ITEM 079_numbers ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/079_numbers.png
----- GROUND TRUTH -----
Invoice No. INV-2023-02845
Date: 27/02/2022
Amount due: $5,227.62
Phone: +1 (693) 538-8956
IBAN: DE79 3707 2981 7248 3474 70
----- OUTPUT A -----
Invoice No. INV-2023-82845

Date: 27/02/2022

Amount due: $5,227.62

Phone: +1 (693) 538-8956

IBAN: DE79 3707 2981 7248 3474 70
----- OUTPUT B -----
Invoice No. INV-2023-02845
Date:27/02/2022
Amount due: $5,227.62
Phone: +1 (693) 538-8956
IBAN: DE79 3707 2981 7248 3474 70


========== ITEM 083_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/083_accented.png
----- GROUND TRUTH -----
Je préfère le thé à la menthe après le dîner.
São Paulo é a maior cidade do Brasil em população.
La reunión será el miércoles a las diez de la mañana.
Æble, øl og smørrebrød er typisk dansk mad.
Señor Núñez llegó tarde a la estación de tren.
----- OUTPUT A -----
Je préfere le thé a la menthe apres le diner.

Sao Paulo ¢é a maior cidade do Brasil em populagéo.
La reuni6n sera el miércoles a las diez de la mafiana.
Able, ol og smerrebrad er typisk dansk mad.

Sefior Nufiez lleg6 tarde a la estacion de tren.
----- OUTPUT B -----
Je préfère le thé à la menthe après le dîner.
São Paulo é a maior cidade do Brasil em população.
La reunión será el miércoles a las diez de la mañana.
AEble, øl og smørrebrød er typisk dansk mad.
Señor Núñez llegó tarde a la estación de tren.


========== ITEM 087_accented ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/087_accented.png
----- GROUND TRUTH -----
El niño comió una manzana mientras leía el periódico.
Die Größe der Datei überschreitet das zulässige Maximum.
Le café de la gare est fermé le dimanche après-midi.
La reunión será el miércoles a las diez de la mañana.
----- OUTPUT A -----
El nifio comi6 una manzana mientras lefa el periédico.

Die GréBe der Datei iiberschreitet das zuldssige Maximum.
Le café de la gare est fermé le dimanche aprés-midi.

La reunion seré el miércoles a las diez de la mafiana.
----- OUTPUT B -----
El niño comió una manzana mientras leía el periódico.
Die Größe der Datei überschreitet das zulässige Maximum.
Le café de la gare est fermé le dimanche après-midi.
La reunión será el miércoles a las diez de la mañana.


========== ITEM 091_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/091_mixed_styles.png
----- GROUND TRUTH -----
Release Notes
Last synced 10:42
Rain is expected through the weekend, with temperatures around 14 degrees.
Keep your dotfiles in version control so a new machine takes minutes, not days.
Most performance problems come from doing work that never needed to happen.
----- OUTPUT A -----
Release Notes

Last synced 10:42

Rain is expected through the weekend, with temperatures around 14 degrees.
Keep your dotfiles in version control so a new machine takes minutes, not days.

Most performance problems come from doing work that never needed to happen.
----- OUTPUT B -----
ReleaseNotes
Last synced 10:42
Rain is expected through the weekend, with temperatures around 14 degrees.
Keep your dotfiles in version control so a new machine takes minutes, not days.
Most performance problems come from doing work that never needed to happen.


========== ITEM 095_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/095_mixed_styles.png
----- GROUND TRUTH -----
Release Notes
Last synced 10:42
The museum's new wing displays maps drawn between 1650 and 1720.
Rain is expected through the weekend, with temperatures around 14 degrees.
The quick brown fox jumps over the lazy dog near the riverbank.
----- OUTPUT A -----
Release Notes
Last synced 10:42
The museum's new wing displays maps drawn between 1650 and 1720.
Rain is expected through the weekend, with temperatures around 14 degrees.
The quick brown fox jumps over the lazy dog near the riverbank.
----- OUTPUT B -----
Release Notes

The museum's new wing displays maps drawn between 1650 and 1720.
Rain is expected through the weekend, with temperatures around 14 degrees.
The quick brown fox jumps over the lazy dog near the riverbank.


========== ITEM 099_mixed_styles ==========
image: /home/rahuldevbanjara/omarchy-ppocr/bench/dataset/099_mixed_styles.png
----- GROUND TRUTH -----
Getting Started
Version 3.1 - October 2024
The quick brown fox jumps over the lazy dog near the riverbank.
The archive contains 1,284 photos taken between 2019 and 2024.
Write the test first, watch it fail, then make it pass with the simplest code.
----- OUTPUT A -----
Getting Started
Version 3.1 - October 2024
The quick brown fox jumps over the lazy dog near the riverbank.
The archive contains 1,284 photos taken between 2019 and 2024.
Write the test first, watch it fail, then make it pass with the simplest code.
----- OUTPUT B -----
Getting Started

Version 3.1 - October 2024

The quick brown fox jumps over the lazy dog near the riverbank.
The archive contains 1,284 photos taken between 2019 and 2024.

Write the test first, watch it fail, then make it pass with the simplest code.
