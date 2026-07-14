"""Static agronomic/veterinary knowledge base.

This is curated reference content (advice text, dipping schedules) — deliberately
NOT AI. It maps model class labels to trilingual treatment advice. In production
this table would be reviewed and signed off by AGRITEX / veterinary services.
"""

from __future__ import annotations

# Crop disease advice keyed by model class label.
# Each entry provides advice in en / sn (Shona) / nd (Ndebele).
CROP_ADVICE: dict[str, dict[str, str]] = {
    "maize_healthy": {
        "en": "No disease detected. Keep monitoring weekly and scout for fall armyworm egg masses.",
        "sn": "Hapana chirwere chawanikwa. Ramba uchitarisa vhiki nevhiki uchitsvaga mazai emhodzi.",
        "nd": "Akulasifo esitholakele. Qhubeka uhlole insimu iviki ngeviki.",
    },
    "maize_lethal_necrosis": {
        "en": "Likely Maize Lethal Necrosis. Rogue and burn infected plants, control thrips/aphids vectors, rotate with non-cereals. Consult AGRITEX before replanting.",
        "sn": "Zvingave Maize Lethal Necrosis. Bvisa uchipisa zvirimwa zvakabatwa, dzora zvipembenene, chinjanisa nezvirimwa zvisiri zviyo. Bvunza AGRITEX.",
        "nd": "Kungenzeka yiMaize Lethal Necrosis. Susa utshise izithombo ezithelelekileyo, ubhubhise izinambuzane. Buza uAGRITEX.",
    },
    "maize_leaf_blight": {
        "en": "Northern Leaf Blight likely. Apply registered fungicide early, use resistant varieties next season, remove crop residue.",
        "sn": "Zvingave Leaf Blight. Shandisa mushonga we-fungicide nekukurumidza, shandisa mbeu dzinorwisa chirwere mwaka unotevera.",
        "nd": "Kungenzeka yiLeaf Blight. Sebenzisa umuthi we-fungicide masinyane, ususe insalela zesivuno.",
    },
    "tomato_early_blight": {
        "en": "Tomato Early Blight likely. Remove lower infected leaves, apply copper/chlorothalonil fungicide, avoid overhead watering, mulch to reduce soil splash.",
        "sn": "Zvingave Tomato Early Blight. Bvisa mashizha akabatwa, shandisa fungicide ye-copper, usadiridzira kubva pamusoro.",
        "nd": "Kungenzeka yiTomato Early Blight. Susa amahlamvu athelelekileyo, usebenzise i-copper fungicide.",
    },
    "tomato_late_blight": {
        "en": "Tomato Late Blight — acts fast. Remove and destroy infected plants immediately, apply protectant fungicide, improve airflow. Consult AGRITEX urgently.",
        "sn": "Tomato Late Blight — inokurumidza. Bvisa uparadze zvirimwa zvakabatwa izvozvi, shandisa fungicide. Bvunza AGRITEX nekukurumidza.",
        "nd": "Tomato Late Blight — isheshayo. Susa ubhubhise izithombo ezithelelekileyo khathesi. Buza uAGRITEX masinyane.",
    },
    "tobacco_mosaic_virus": {
        "en": "Tobacco Mosaic Virus suspected. Remove infected plants, disinfect hands/tools, control aphids, do not use tobacco products while handling crop.",
        "sn": "Zvingave Tobacco Mosaic Virus. Bvisa zvirimwa zvakabatwa, geza maoko nemidziyo, dzora zvipembenene.",
        "nd": "Kungenzeka yiTobacco Mosaic Virus. Susa izithombo ezithelelekileyo, ugezise izandla lamathulusi.",
    },
}

# Livestock condition advice keyed by class label.
LIVESTOCK_ADVICE: dict[str, dict[str, str]] = {
    "cattle_healthy": {
        "en": "Body condition looks normal. Maintain dipping schedule and mineral licks.",
        "sn": "Mombe inoratidza kunge yakanaka. Ramba uchidipa nekupa mineral.",
        "nd": "Inkomo ikhangeleka iphilile. Qhubeka ngokugezisa lokunika iminerali.",
    },
    "cattle_heavy_tick_load": {
        "en": "Heavy tick load — high theileriosis (January disease) risk. Dip/spray now with registered acaricide, repeat per schedule, watch for fever, swollen lymph nodes, weakness. Call your vet.",
        "sn": "Makwashamu akawanda — njodzi ye-January disease. Dipa/pfapfaidza nemushonga izvozvi, tarisa fivha nekuzvimba. Fonera veterinary.",
        "nd": "Umkhaza omunengi — ingozi ye-January disease. Gezisa ngomuthi khathesi, uqaphele umkhuhlane. Biza udokotela wezifuyo.",
    },
    "cattle_skin_lesion": {
        "en": "Skin lesions detected — possible lumpy skin disease or dermatophilosis. Isolate the animal, keep wounds clean, consult a veterinarian for diagnosis and vaccination advice.",
        "sn": "Maronda paganda — zvingava lumpy skin disease. Tsaura mombe, chengetedza maronda akachena, bvunza chiremba wemhuka.",
        "nd": "Amanxeba esikhumbeni — kungenzeka yilumpy skin disease. Yehlukanise isifuyo, ubone udokotela.",
    },
}

# Dipping / vaccination reference schedule (rule-based content for SMS tips).
LIVESTOCK_SCHEDULE = {
    "dipping_wet_season": "During the wet season (Nov-Apr) dip cattle WEEKLY to control ticks and prevent January disease.",
    "dipping_dry_season": "During the dry season (May-Oct) dip cattle every FORTNIGHT.",
    "vaccination_anthrax": "Vaccinate against anthrax and blackleg annually before the rains.",
}


def crop_advice(label: str, language: str = "en") -> tuple[str, dict[str, str]]:
    """Return (localized advice, full i18n dict) for a crop class label."""
    entry = CROP_ADVICE.get(label, {})
    text = entry.get(language) or entry.get("en") or "Consult AGRITEX for advice."
    return text, entry


def livestock_advice(label: str, language: str = "en") -> tuple[str, dict[str, str]]:
    """Return (localized advice, full i18n dict) for a livestock class label."""
    entry = LIVESTOCK_ADVICE.get(label, {})
    text = entry.get(language) or entry.get("en") or "Consult a veterinarian."
    return text, entry
