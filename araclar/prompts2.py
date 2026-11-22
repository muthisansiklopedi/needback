from prompts import STYLE_169, STYLE_916, NEG
# Sıra, senaryodaki bölüm sırasıyla aynı olmalı.
B1 = {
 "hook": [
  ("Sönen şehir", "night city skyline where districts go dark one by one, aerial view"),
  ("Hastane uyarısı", "hospital corridor at night with computer screens glowing red, empty gurney, no people visible"),
 ],
 "stuxnet": [
  ("Yer altı tesisi", "underground industrial facility in a desert, long rows of tall silver centrifuges, cold lighting"),
  ("USB bellek", "macro shot of a USB flash drive being inserted into an old industrial computer, dust in the light beam"),
  ("Yalan söyleyen ekran", "control room monitor showing calm green gauges while in the background a machine sparks"),
 ],
 "ukrayna": [
  ("Karlı kasaba", "snowy Eastern European town at dusk, all windows going dark, power lines in the foreground"),
  ("Kendi kendine hareket eden imleç", "operator's hands raised away from a mouse while the cursor on screen moves by itself over a power grid diagram"),
 ],
 "wannacry": [
  ("Kırmızı fidye ekranı", "row of office computers all showing a bright red lock screen, abstract, no readable text"),
  ("Ambulans yönlendirmesi", "ambulance at night outside a hospital entrance, blue lights reflecting on wet pavement"),
  ("10 dolarlık alan adı", "young researcher's desk at night, laptop with a single glowing domain bar, coffee mug, face not visible"),
 ],
 "notpetya": [
  ("Duran liman", "huge container port at dusk with idle cranes and stacked containers, no movement, ominous sky"),
  ("Boş ofis", "open-plan office with every screen black, chairs pushed back, papers on the floor"),
  ("Gana'daki sunucu", "single server rack in a small dim office in West Africa, one green light glowing"),
 ],
 "solarwinds": [
  ("Güncellemenin içindeki göz", "software update package box opening to reveal a glowing eye inside, dark background"),
  ("Devlet binaları", "neoclassical government buildings at night with faint digital network lines connecting them"),
 ],
 "colonial": [
  ("Benzin kuyruğu", "long line of cars at a gas station with 'out of fuel' style signage without readable text, evening"),
  ("Boru hattı", "industrial fuel pipeline stretching across fields to the horizon at sunset, valves closed"),
  ("Unutulmuş şifre", "old login screen with a single glowing password field, cobwebs on the monitor edge"),
 ],
 "final": [
  ("Altı dosya", "six case files laid on a dark table, each stamped with a red seal, overhead view"),
  ("Mavi ekranlı havalimanı", "airport departure hall with every display showing a plain blue screen, travelers' silhouettes waiting"),
 ],
}

B2 = {
 "hook": [
  ("Isı dalgalı pist", "fighter jet taking off with heat haze over the runway, low angle, dusk"),
  ("Boş kokpit", "close-up of a modern fighter jet cockpit with no pilot inside, displays glowing"),
 ],
 "nesiller": [
  ("Nesillerin dizilişi", "lineup of fighter jet silhouettes from 1940s propeller plane to modern stealth fighter, side view, museum lighting"),
  ("Radar dağıtan gövde", "stealth fighter with radar waves visualized as orange lines scattering off its angular surfaces"),
  ("Sensör füzyonu", "pilot helmet visor reflecting a fused tactical map with icons, abstract, no readable text"),
 ],
 "f35": [
  ("Üretim hattı*", "fighter jet assembly line in a vast clean hangar, workers in silhouette"),
  ("Hava savunma sistemi", "long-range air defense missile launchers raised on trucks under a grey sky"),
  ("Boşluk", "empty hangar with a single spotlight on the floor where a jet should be"),
 ],
 "altinci": [
  ("Kuyruksuz konsept", "futuristic tailless sixth generation fighter concept flying above clouds at sunrise"),
  ("Sadık kanatlar", "crewed fighter jet leading three smaller unmanned jets in V formation, sunset"),
  ("Komuta merkezi kokpit", "pilot's view with holographic overlays showing positions of escorting drones"),
 ],
 "kaan": [
  ("Hangardan çıkış*", "new twin-engine stealth fighter rolled out of a hangar into bright light, crowd silhouettes"),
  ("İlk uçuş*", "twin-engine stealth fighter prototype climbing after takeoff, chase plane nearby"),
  ("İç silah yuvası*", "underside of a stealth fighter with internal weapons bay doors open, studio lighting"),
  ("Motor testi", "jet engine on a test stand with afterburner glowing, engineers behind glass"),
  ("İnsanlı-insansız ekip*", "stealth fighter flying with a jet-powered unmanned combat aircraft and a flying-wing drone"),
 ],
 "yorum": [
  ("Yorum masası", "dim studio desk with a microphone, a model fighter jet and a small Turkish flag, shallow depth of field"),
  ("Maraton", "long runway stretching to the horizon at dawn, single jet silhouette at the far end"),
 ],
 "kapanis": [
  ("Kapanış", "pilot silhouette standing on a tarmac looking at a sky full of distant unmanned aircraft lights"),
 ],
}

R1 = [
 ("USB düşüyor", "USB flash drive falling onto a dark metal desk in slow motion, dramatic rim light"),
 ("İnternetsiz tesis", "desert facility entrance at night, guarded gate, no network antennas"),
 ("Kodun yayılması", "red code spreading like veins across a dark circuit board"),
 ("Yalan söyleyen ekran", "centrifuges spinning chaotically while a monitor shows calm green gauges"),
 ("Kıvılcım", "broken centrifuge with sparks flying, dark industrial hall"),
 ("Kapanış kartı", "dark slate-green background with an orange abstract wall-and-embrasure pattern, empty center for logo"),
]
R2 = [
 ("Çarpılı silüet*", "silhouette of a stealth fighter against a grey sky with a large red X overlay shape"),
 ("Parça üretimi", "close-up of aircraft fuselage parts on a factory floor, precise machining"),
 ("Hangar kapısı", "giant hangar doors opening, light pouring in, silhouette of a fighter jet inside"),
 ("İlk uçuş*", "stealth fighter prototype taking off, landing gear retracting, golden hour"),
 ("Ekip uçuşu*", "stealth fighter flying with two unmanned combat aircraft, top-down view over clouds"),
 ("Kapanış kartı", "dark slate-green background with an orange abstract wall-and-embrasure pattern, empty center for logo"),
]
R3 = [
 ("Benzin kuyruğu", "long line of cars at a gas station at dusk, red brake lights"),
 ("Sızıntı listesi", "endless scrolling list of blurred email addresses on a dark screen, one line glowing orange"),
 ("Kontrol sitesi", "screen recording placeholder: generic browser with a single search field, clean interface"),
 ("Telefonda kontrol", "screen recording placeholder: generic phone password settings screen with a security warning icon"),
 ("Üç adım", "three glowing icons on dark background: key being changed, crossed duplicate keys, phone with a shield"),
 ("Kaydet", "phone with a bookmark icon glowing orange, dark background"),
]
