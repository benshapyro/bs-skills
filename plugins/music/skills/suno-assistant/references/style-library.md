# Style Library

Lookup material for building Suno prompts: artist translation, song structures by genre, ready-to-adapt style templates, and how to read vague requests. Pull what you need; don't dump the whole file into a prompt.

## Contents
1. Artist → sonic-descriptor translation
2. Genre-adaptive song structures
3. Style-line templates (vocal)
4. Style-line templates (instrumental)
5. Reading vague requests

---

## 1. Artist → sonic-descriptor translation

Never put an artist's name in the final Suno prompt. Translate the *sound* instead — it gives finer control and avoids style-attribution issues. Acknowledge the reference, name the 2–3 qualities you're pulling, then build from descriptors.

| If they say… | Translate to… |
|---|---|
| "Like Radiohead" | Atmospheric art-rock, falsetto vocals, electronic textures, melancholic, experimental arrangements, ambient undertones |
| "Like Adele" | Powerful soulful belting, piano-driven ballad, cinematic production, emotional crescendos, rich alto voice, intimate verses into anthemic chorus |
| "Daft Punk vibes" | French house, vocoder-processed vocals, funky basslines, four-on-the-floor groove, filtered disco samples, analog synth warmth |
| "Like Bon Iver" | Indie folk, layered falsetto harmonies, intimate production, atmospheric reverb, acoustic with electronic textures, sparse arrangements building to lush climaxes |
| "Hans Zimmer style" | Epic orchestral, brass hits, driving percussion, layered strings, tension-building ostinatos, cinematic sweep, powerful dynamics |
| "Lo-fi study beats" | Lo-fi hip hop, vinyl crackle, mellow piano chops, tape saturation, jazzy chords, relaxed drums, warm dusty texture |
| "Classic Motown" | Vintage 60s soul, warm upright bass, tambourine groove, lush strings, brass stabs, call-and-response vocals, analog warmth |
| "80s synth-pop" | Analog synthesizers, gated-reverb drums, arpeggiated basslines, bright pads, new-wave energy, polished nostalgic production |
| "90s grunge" | Heavy distorted guitars, raw vocals, quiet-loud dynamics, drop-tuned, live-room drums, unpolished angst |
| "Modern trap" | 808 sub-bass, hi-hat rolls, sparse dark pads, triplet flows, hard-hitting kicks, atmospheric ad-libs |
| "Taylor Swift (pop era)" | Polished synth-pop, bright conversational female vocals, layered harmonies, punchy programmed drums, big singalong chorus, radio production |
| "Billie Eilish" | Dark bedroom-pop, breathy close-mic'd vocals, minimal sub-heavy production, whispered intimacy, sparse haunting arrangement |

### Build your own translation

Break any artist into five components and describe each:
1. **Vocal character** — range, texture, delivery (raspy tenor, breathy alto, spoken-word)
2. **Core instruments** — what drives the sound
3. **Production aesthetic** — era, polish level, sonic signature (lo-fi tape vs. glossy radio)
4. **Emotional tone** — mood, energy, attitude
5. **Structural tendencies** — how their songs are built (slow burn, immediate hook)

---

## 2. Genre-adaptive song structures

Defaults — adjust when the user specifies. Section tags go in the Lyrics field, each on its own line.

**Pop / Dance**
`[Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Verse 2] → [Pre-Chorus] → [Chorus] → [Bridge] → [Chorus] → [Outro]`
Pre-choruses give the chorus its lift.

**Rock / Alternative**
`[Intro] → [Verse 1] → [Chorus] → [Verse 2] → [Chorus] → [Bridge] → [Guitar Solo] → [Chorus] → [Outro]`
Rock expects a bridge and an instrumental break; add a solo for classic rock.

**Electronic / EDM**
`[Intro] → [Build] → [Drop] → [Breakdown] → [Build] → [Drop] → [Outro]`
Lives and dies by the drop.

**Hip-Hop / Rap**
`[Intro] → [Verse 1] → [Hook] → [Verse 2] → [Hook] → [Verse 3] → [Hook] → [Outro]`
Use `[Hook]` not `[Chorus]`; verses carry the weight; consider `[Ad-libs]`.

**R&B / Soul**
`[Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Verse 2] → [Chorus] → [Bridge] → [Chorus] → [Ad-lib Outro]`
Ad-libs and runs, especially over the final chorus.

**Country**
`[Intro] → [Verse 1] → [Chorus] → [Verse 2] → [Chorus] → [Bridge] → [Instrumental Break] → [Chorus] → [Outro]`
Storytelling verses; fiddle/steel break.

**Ballad (any genre)**
`[Intro] → [Verse 1] → [Verse 2] → [Chorus] → [Verse 3] → [Chorus] → [Bridge] → [Final Chorus] → [Outro]`
Can delay the chorus for emotional build.

**Cinematic / Orchestral (instrumental)**
`[Intro] → [Theme A] → [Development] → [Climax] → [Reprise] → [Outro]`
Build tension, peak, resolve.

**Ambient / Downtempo (instrumental)**
`[Intro] → [Theme A] → [Breakdown] → [Build] → [Theme B] → [Outro]`
Gradual evolution; avoid abrupt transitions.

For non-standard instrumental structures (loop points, spatial arcs, journey-based naming), see `advanced-patterns.md`.

---

## 3. Style-line templates (vocal)

Copy and adapt. Each is 4–7 descriptors, defining word first.

- **Indie folk** — `Indie folk, acoustic guitar-driven, warm male vocals, introspective, 100 BPM, fingerpicked guitar, gentle harmonies, intimate production with light reverb`
- **Modern pop** — `Modern pop, upbeat, bright female vocals, synth-heavy, 120 BPM, radio-ready mix, punchy drums, catchy hooks`
- **90s alt-rock** — `90s alternative rock, grunge-influenced, raw male vocals, distorted guitars, live drums, garage energy, quiet-loud dynamics`
- **Contemporary R&B** — `Contemporary R&B, smooth, breathy female vocals, neo-soul grooves, warm keys, 85 BPM, intimate production`
- **Progressive house** — `Progressive house, 128 BPM, euphoric builds, punchy drops, sidechained bass, festival-ready, atmospheric pads`
- **Orchestral pop** — `Orchestral pop, epic, powerful mixed vocals, strings and piano-led, building dynamics, dramatic crescendos`
- **Gospel-soul ballad** — `Gospel-soul ballad, powerful female belt, church organ, choir swells, 70 BPM, emotional crescendo, uplifting`
- **Reggae-Afrobeat fusion** — `Reggae-Afrobeat fusion, laid-back groove, male vocals, offbeat guitar, afro percussion, 95 BPM, sunny`
- **Lo-fi hip-hop (with vocals)** — `Lo-fi hip hop, chill, soft-spoken vocals, vinyl crackle, mellow piano chops, 85 BPM, late-night, dusty tape warmth`
- **2000s pop-punk** — `2000s pop-punk, fast 170 BPM, nasally male vocals, palm-muted guitars, angsty, arena-ready chorus`

---

## 4. Style-line templates (instrumental)

Each opens with `instrumental, no vocals` — this is what stops Suno adding a vocal. Skip all vocal-range and vocal-texture words.

- **Cinematic post-rock** — `Instrumental, no vocals, cinematic post-rock, tremolo-picked delay guitars, swelling strings, room-miked drums, wide stereo, slow-building crescendos, emotional catharsis`
- **Jazz fusion** — `Instrumental, no vocals, jazz fusion, complex Rhodes chords, syncopated drums, warm analog synths, sophisticated mid-tempo groove`
- **Ambient electronic** — `Instrumental, no vocals, ambient electronic, lush synth pads, tape warble, subtle beats, nostalgic warmth, downtempo, wide stereo field`
- **Orchestral hybrid** — `Instrumental, no vocals, orchestral hybrid, epic brass fanfares, driving percussion, soaring strings, triumphant, powerful dynamics`
- **Lo-fi study beats** — `Instrumental, no vocals, lo-fi hip hop, dusty vinyl texture, mellow piano loops, tape hiss, 75 BPM, relaxing late-night`
- **Synthwave** — `Instrumental, no vocals, synthwave, driving arpeggios, gated-reverb drums, analog bass, neon-noir atmosphere, 110 BPM, retro-futuristic`
- **Neoclassical** — `Instrumental, no vocals, neoclassical, intimate piano, subtle strings, electronic textures, melancholic, spacious production`
- **Chiptune / 8-bit** — `Instrumental, no vocals, chiptune adventure, retro synth leads, bouncy arpeggios, energetic, nostalgic 8-bit charm, 140 BPM`
- **Boss-battle orchestral** — `Instrumental, no vocals, orchestral metal, epic boss-battle, D minor, 140 BPM, aggressive strings, pounding timpani, distorted guitars, choir stabs, menacing`

For instrumental structure tags, `[Theme A]` / `[Theme B]` / `[Development]` / `[Climax]` / `[Breakdown]` work well in place of verse/chorus. Full toolkit in `advanced-patterns.md`.

---

## 5. Reading vague requests

| They say… | They probably want… |
|---|---|
| "Something chill" | Downtempo, relaxed groove, laid-back production |
| "Background music for X" | Instrumental, mood matched to the use case |
| "Epic / cinematic" | Orchestral hybrid, building dynamics, dramatic |
| "Vibey" | Atmospheric, mood-focused, textural |
| "Catchy" | Strong hooks, pop sensibility, memorable melody |
| "Raw / authentic" | Minimal production, organic, unpolished |
| "Like 90s…" | Era-specific production + genre conventions |
| "Happy / upbeat" | Major key, faster tempo, bright production |
| "Dark / moody" | Minor key, slower tempo, atmospheric |

When you infer from one of these, say the assumption out loud ("I'm reading 'chill' as downtempo and relaxed — shout if you meant something more upbeat") so they can correct fast.
