"""Collection of datasets representing viruses known to infect humans.

The sequences in these datasets were automatically downloaded
from GenBank by filtering its list of all viral accessions (taxId:10239)
for those lineages that are listed with human as a host.
"""

import sys

from catch.datasets import DatasetCollection

__author__ = 'Hayden Metsky <hayden@mit.edu>'


DATASETS = [
    'achimota_rubulavirus_1',
    'achimota_rubulavirus_2',
    'adeno-associated_dependoparvovirus_a',
    'adeno-associated_dependoparvovirus_b',
    'aedes_flavivirus',
    'african_green_monkey_simian_foamy',
    'aguacate',
    'aichivirus_a',
    'akabane_orthobunyavirus',
    'alagoas_vesiculovirus',
    'alajuela_orthobunyavirus',
    'allpahuayo_mammarenavirus',
    'alphapapillomavirus_4',
    'alphapapillomavirus_7',
    'alphapapillomavirus_9',
    'ambe',
    'andes_orthohantavirus',
    'anhanga',
    'anopheles_a_orthobunyavirus',
    'anopheles_b_orthobunyavirus',
    'apoi',
    'aravan_lyssavirus',
    'argentinian_mammarenavirus',
    'aroa',
    'arrabida',
    'arumowot',
    'asama_orthohantavirus',
    'australian_bat_lyssavirus',
    'avian_avulavirus_10',
    'avian_avulavirus_11',
    'avian_avulavirus_12',
    'avian_avulavirus_13',
    'avian_avulavirus_14',
    'avian_avulavirus_15',
    'avian_avulavirus_16',
    'avian_avulavirus_17',
    'avian_avulavirus_18',
    'avian_avulavirus_19',
    'avian_avulavirus_1',
    'avian_avulavirus_3',
    'avian_avulavirus_4',
    'avian_avulavirus_5',
    'avian_avulavirus_6',
    'avian_avulavirus_7',
    'avian_avulavirus_8',
    'avian_avulavirus_9',
    'avian_gyrovirus_2',
    'avian_metapneumovirus',
    'bagaza',
    'banna',
    'banzi',
    'barmah_forest',
    'batama_orthobunyavirus',
    'bat_hepacivirus',
    'bat_mumps_rubulavirus',
    'bat_sapovirus_tlc58--hk',
    'bayou_orthohantavirus',
    'bear_canyon_mammarenavirus',
    'beilong',
    'betapapillomavirus_1',
    'betapapillomavirus_2',
    'betapapillomavirus_3',
    'betapapillomavirus_4',
    'betapapillomavirus_5',
    'betapapillomavirus_6',
    'bhanja',
    'bimiti_orthobunyavirus',
    'black_creek_canal_orthohantavirus',
    'bokeloh_bat_lyssavirus',
    'bouboui',
    'bovine_hepacivirus',
    'bovine_respirovirus_3',
    'bowe_orthohantavirus',
    'brazilian_mammarenavirus',
    'brazoran',
    'bruges_orthohantavirus',
    'bujaru_phlebovirus',
    'bundibugyo_ebolavirus',
    'bunyamwera_orthobunyavirus',
    'bwamba_orthobunyavirus',
    'cacipacore',
    'california_encephalitis_orthobunyavirus',
    'california_reptarenavirus',
    'cali_mammarenavirus',
    'candiru_phlebovirus',
    'canine_morbillivirus',
    'cano_delgadito_orthohantavirus',
    'cao_bang_orthohantavirus',
    'capim_orthobunyavirus',
    'caraparu_orthobunyavirus',
    'cardiovirus_a',
    'cardiovirus_b',
    'catu_orthobunyavirus',
    'cedar_henipavirus',
    'cell_fusing_agent',
    'cetacean_morbillivirus',
    'chandipura_vesiculovirus',
    'chaoyang',
    'chapare_mammarenavirus',
    'chicken_anemia',
    'chikungunya',
    'choclo_orthohantavirus',
    'circular_ssdna_virus_hv-cv1',
    'cocal_vesiculovirus',
    'colorado_tick_fever',
    'corriparta',
    'cosavirus_a',
    'cosavirus_b',
    'cosavirus_d',
    'cosavirus_e',
    'cosavirus_f',
    'cowpox',
    'crimean-congo_hemorrhagic_fever_orthonairovirus',
    'culex_flavivirus',
    'cupixi_mammarenavirus',
    'dabieshan_orthohantavirus',
    'dengue',
    'dera_ghazi_khan_orthonairovirus',
    'dhori_thogotovirus',
    'dobrava-belgrade_orthohantavirus',
    'donggang',
    'dugbe_orthonairovirus',
    'duvenhage_lyssavirus',
    'eastern_equine_encephalitis',
    'edge_hill',
    'ekpoma_1_tibrovirus',
    'ekpoma_2_tibrovirus',
    'el_moro_canyon_orthohantavirus',
    'entebbe_bat',
    'enterovirus_a',
    'enterovirus_b',
    'enterovirus_c',
    'enterovirus_d',
    'enterovirus_e',
    'equine_rhinitis_a',
    'erbovirus_a',
    'european_bat_1_lyssavirus',
    'european_bat_2_lyssavirus',
    'everglades',
    'eyach',
    'feline_morbillivirus',
    'flexal_mammarenavirus',
    'foot-and-mouth_disease',
    'fugong_orthohantavirus',
    'fusong_orthohantavirus',
    'gadgets_gully',
    'gairo_mammarenavirus',
    'gamboa_orthobunyavirus',
    'gammapapillomavirus_18',
    'gammapapillomavirus_24',
    'gammapapillomavirus_27',
    'gemycircularvirus_hv-gcv1',
    'getah',
    'giant_panda_anellovirus',
    'giessen_reptarenavirus',
    'golden_reptarenavirus',
    'goose_paramyxovirus_sf02',
    'gorilla_anellovirus',
    'great_island',
    'guajara_orthobunyavirus',
    'guama_orthobunyavirus',
    'guanarito_mammarenavirus',
    'guaroa_orthobunyavirus',
    'gyrovirus_4',
    'gyrovirus_gyv3',
    'gyrovirus_gyv7-sf',
    'gyrovirus_tu243',
    'gyrovirus_tu789',
    'hanko',
    'hantaan_orthohantavirus',
    'hantavirus_z10',
    'hazara_orthonairovirus',
    'heartland',
    'hendra_henipavirus',
    'hepacivirus_a',
    'hepacivirus_b',
    'hepacivirus_c',
    'hepacivirus_d',
    'hepacivirus_f',
    'hepacivirus_i',
    'hepacivirus_j',
    'hepacivirus_k',
    'hepacivirus_l',
    'hepacivirus_m',
    'hepacivirus_n',
    'hepatitis_b',
    'hepatitis_delta',
    'hepatovirus_a',
    'highlands_j',
    'hughes_orthonairovirus',
    'human_alphaherpesvirus_1',
    'human_alphaherpesvirus_2',
    'human_alphaherpesvirus_3',
    'human_associated_circovirus_1',
    'human_associated_cyclovirus_10',
    'human_associated_cyclovirus_11',
    'human_associated_cyclovirus_12',
    'human_associated_cyclovirus_1',
    'human_associated_cyclovirus_2',
    'human_associated_cyclovirus_3',
    'human_associated_cyclovirus_4',
    'human_associated_cyclovirus_5',
    'human_associated_cyclovirus_6',
    'human_associated_cyclovirus_7',
    'human_associated_cyclovirus_8',
    'human_associated_cyclovirus_9',
    'human_associated_gemykibivirus_1',
    'human_associated_gemykibivirus_2',
    'human_associated_gemykibivirus_5',
    'human_associated_gemyvongvirus_1',
    'human_betaherpesvirus_5',
    'human_betaherpesvirus_6a',
    'human_betaherpesvirus_6b',
    'human_betaherpesvirus_7',
    'human_coronavirus_229e',
    'human_coronavirus_hku1',
    'human_coronavirus_nl63',
    'human_endogenous_retrovirus_k',
    'human_fecal_virus_jorvi2',
    'human_fecal_virus_jorvi3',
    'human_fecal_virus_jorvi4',
    'human_gammaherpesvirus_4',
    'human_gammaherpesvirus_8',
    'human_immunodeficiency_virus_1',
    'human_immunodeficiency_virus_2',
    'human_mastadenovirus_a',
    'human_mastadenovirus_b',
    'human_mastadenovirus_c',
    'human_mastadenovirus_d',
    'human_mastadenovirus_e',
    'human_mastadenovirus_f',
    'human_mastadenovirus_g',
    'human_metapneumovirus',
    'human_orthopneumovirus',
    'human_papillomavirus',
    'human_papillomavirus_type_85',
    'human_picobirnavirus',
    'human_polyomavirus_1',
    'human_polyomavirus_2',
    'human_polyomavirus_3',
    'human_polyomavirus_4',
    'human_polyomavirus_5',
    'human_respirovirus_1',
    'human_respirovirus_3',
    'human_rubulavirus_2',
    'human_rubulavirus_4',
    'human_smacovirus_1',
    'ikoma_lyssavirus',
    'ilheus',
    'imjin_orthohantavirus',
    'indiana_vesiculovirus',
    'ippy_mammarenavirus',
    'irkut_lyssavirus',
    'isfahan_vesiculovirus',
    'japanese_encephalitis',
    'jeju_orthohantavirus',
    'jugra',
    'j-virus',
    'kabuto_mountain',
    'kadam',
    'kadipiro',
    'kaeng_khoi_orthobunyavirus',
    'kairi_orthobunyavirus',
    'kamiti_river',
    'kasokero_orthonairovirus',
    'kedougou',
    'kenkeme_orthohantavirus',
    'keterah_orthonairovirus',
    'khabarovsk_orthohantavirus',
    'khujand_lyssavirus',
    'kokobera',
    'koongol_orthobunyavirus',
    'kyasanur_forest_disease',
    'lagos_bat_lyssavirus',
    'laguna_negra_orthohantavirus',
    'laibin_orthohantavirus',
    'langat',
    'lassa_mammarenavirus',
    'latino_mammarenavirus',
    'lebombo',
    'le_dantec_ledantevirus',
    'leopards_hill',
    'liao_ning',
    'lleida_bat_lyssavirus',
    'lloviu_cuevavirus',
    'loei_river_mammarenavirus',
    'louping_ill',
    'lujo_mammarenavirus',
    'luna_mammarenavirus',
    'lunk_mammarenavirus',
    'luxi_orthohantavirus',
    'lymphocytic_choriomeningitis_mammarenavirus',
    'lyssavirus_ozernoe',
    'macaca_mulatta_polyomavirus_1',
    'macaque_simian_foamy',
    'machupo_mammarenavirus',
    'madrid_orthobunyavirus',
    'main_drain_orthobunyavirus',
    'mamastrovirus_1',
    'mamastrovirus_6',
    'mamastrovirus_8',
    'mamastrovirus_9',
    'mammalian_orthoreovirus',
    'mammalian_rubulavirus_5',
    'manzanilla_orthobunyavirus',
    'maporal_orthohantavirus',
    'mapuera_rubulavirus',
    'maraba_vesiculovirus',
    'marburg_marburgvirus',
    'marituba_orthobunyavirus',
    'mayaro',
    'meaban',
    'measles_morbillivirus',
    'menangle_rubulavirus',
    'mercadeo',
    'middle_east_respiratory_syndrome-related_coronavirus',
    'mobala_mammarenavirus',
    'modoc',
    'mojiang_henipavirus',
    'mokola_lyssavirus',
    'molluscum_contagiosum',
    'monkeypox',
    'montana_myotis_leukoencephalitis',
    'montano_orthohantavirus',
    'mopeia_lassa_virus_reassortant_29',
    'mopeia_mammarenavirus',
    'morogoro_mammarenavirus',
    'mossman',
    'mosso_das_pedras',
    'mucambo',
    'mumps_rubulavirus',
    'mupapillomavirus_1',
    'murine_respirovirus',
    'murray_valley_encephalitis',
    'nairobi_sheep_disease_orthonairovirus',
    'nariva',
    'ndumu',
    'nelson_bay_orthoreovirus',
    'new_jersey_vesiculovirus',
    'nipah_henipavirus',
    'norwalk',
    'norway_rat_hepacivirus_1',
    'norway_rat_hepacivirus_2',
    'nounane',
    'nova_orthohantavirus',
    'ntaya',
    'nyando_orthobunyavirus',
    'ochlerotatus_caspius_flavivirus',
    'oliveros_mammarenavirus',
    'omsk_hemorrhagic_fever',
    'onyong-nyong',
    'ordinary_reptarenavirus',
    'orf',
    'oriboca_orthobunyavirus',
    'oropouche_orthobunyavirus',
    'orthohepevirus_a',
    'orthohepevirus_b',
    'orthohepevirus_c',
    'orthohepevirus_d',
    'orungo',
    'palm_creek',
    'paraguayan_mammarenavirus',
    'paraiso_escondido',
    'parechovirus_a',
    'parechovirus_b',
    'parramatta_river',
    'patois_orthobunyavirus',
    'pegivirus_a',
    'pegivirus_c',
    'pegivirus_h',
    'phnom_penh_bat',
    'phocine_morbillivirus',
    'pirital_mammarenavirus',
    'piry_vesiculovirus',
    'piscihepevirus_a',
    'pixuna',
    'porcine_respirovirus_1',
    'porcine_rubulavirus',
    'powassan',
    'primate_erythroparvovirus_1',
    'primate_t-lymphotropic_virus_1',
    'primate_t-lymphotropic_virus_2',
    'primate_t-lymphotropic_virus_3',
    'prospect_hill_orthohantavirus',
    'punta_toro_phlebovirus',
    'puumala_orthohantavirus',
    'qalyub_orthonairovirus',
    'quang_binh',
    'quezon_orthohantavirus',
    'rabies_lyssavirus',
    'razdan',
    'reptilian_ferlavirus',
    'respiratory_syncytial',
    'reston_ebolavirus',
    'rhinovirus_a',
    'rhinovirus_b',
    'rhinovirus_c',
    'rift_valley_fever_phlebovirus',
    'rinderpest_morbillivirus',
    'rio_bravo',
    'rio_negro',
    'rockport_orthohantavirus',
    'rodent_hepacivirus',
    'rodent_torque_teno_virus_2',
    'rosavirus_a',
    'ross_river',
    'rotavirus_a',
    'rotavirus_b',
    'rotavirus_c',
    'rotavirus_f',
    'rotavirus_g',
    'rotavirus_h',
    'rotavirus_i',
    'royal_farm',
    'rubella',
    'ryukyu_mammarenavirus',
    'saboya',
    'saint_louis_encephalitis',
    'sakhalin_orthonairovirus',
    'salehabad_phlebovirus',
    'salem',
    'salivirus_a',
    'salmon_aquaparamyxovirus',
    'sandfly_fever_naples_phlebovirus',
    'sandfly_fever_sicilian',
    'sangassou_orthohantavirus',
    'sapporo',
    'sathuperi_orthobunyavirus',
    'saumarez_reef',
    'seal_anellovirus_2',
    'seal_anellovirus_3',
    'seal_anellovirus_tffn--usa--2006',
    'semliki_forest',
    'seoul_orthohantavirus',
    'sepik',
    'serra_do_navio_mammarenavirus',
    'severe_acute_respiratory_syndrome-related_coronavirus',
    'sewage_derived_gemygorvirus_1',
    'sfts_phlebovirus',
    'shamonda_orthobunyavirus',
    'shimoni_bat_lyssavirus',
    'shuni_orthobunyavirus',
    'simbu_orthobunyavirus',
    'simian_foamy',
    'simian_immunodeficiency',
    'simian_rubulavirus',
    'simian_torque_teno_virus_30',
    'simian_torque_teno_virus_31',
    'simian_torque_teno_virus_32',
    'simian_torque_teno_virus_33',
    'simian_torque_teno_virus_34',
    'sindbis',
    'sin_nombre_orthohantavirus',
    'small_anellovirus',
    'small_ruminant_morbillivirus',
    'solwezi_mammarenavirus',
    'sosuga_rubulavirus',
    'souris_mammarenavirus',
    'spanish_goat_encephalitis',
    'spondweni',
    'sudan_ebolavirus',
    'tacaiuma_orthobunyavirus',
    'tacaribe_mammarenavirus',
    'tai_forest_ebolavirus',
    'tailam',
    'tamana_bat',
    'tamiami_mammarenavirus',
    'tanapox',
    'tapara',
    'tembusu',
    'tete_orthobunyavirus',
    'thailand_orthohantavirus',
    'thiafora_orthonairovirus',
    'thogoto_thogotovirus',
    'tho',
    'thottapalayam_orthohantavirus',
    'tick-borne_encephalitis',
    'tioman_rubulavirus',
    'tofla',
    'tonate',
    'toros',
    'torque_teno_canis',
    'torque_teno_douroucouli',
    'torque_teno_felis',
    'torque_teno_felis_virus_2',
    'torque_teno_indri_virus_1',
    'torque_teno_leptonychotes_weddellii_virus-1',
    'torque_teno_leptonychotes_weddellii_virus-2',
    'torque_teno_midi_virus_10',
    'torque_teno_midi_virus_11',
    'torque_teno_midi_virus_12',
    'torque_teno_midi_virus_13',
    'torque_teno_midi_virus_14',
    'torque_teno_midi_virus_15',
    'torque_teno_midi_virus_1',
    'torque_teno_midi_virus_2',
    'torque_teno_midi_virus_3',
    'torque_teno_midi_virus_4',
    'torque_teno_midi_virus_5',
    'torque_teno_midi_virus_6',
    'torque_teno_midi_virus_7',
    'torque_teno_midi_virus_8',
    'torque_teno_midi_virus_9',
    'torque_teno_mini_virus_10',
    'torque_teno_mini_virus_11',
    'torque_teno_mini_virus_12',
    'torque_teno_mini_virus_18',
    'torque_teno_mini_virus_1',
    'torque_teno_mini_virus_2',
    'torque_teno_mini_virus_3',
    'torque_teno_mini_virus_4',
    'torque_teno_mini_virus_5',
    'torque_teno_mini_virus_6',
    'torque_teno_mini_virus_7',
    'torque_teno_mini_virus_8',
    'torque_teno_mini_virus_9',
    'torque_teno_mini_virus_ala22',
    'torque_teno_mini_virus_alh8',
    'torque_teno_sus_virus_1a',
    'torque_teno_sus_virus_1b',
    'torque_teno_sus_virus_k2a',
    'torque_teno_sus_virus_k2b',
    'torque_teno_tamarin',
    'torque_teno',
    'torque_teno_tupaia',
    'torque_teno_virus_10',
    'torque_teno_virus_11',
    'torque_teno_virus_12',
    'torque_teno_virus_13',
    'torque_teno_virus_14',
    'torque_teno_virus_15',
    'torque_teno_virus_16',
    'torque_teno_virus_19',
    'torque_teno_virus_1',
    'torque_teno_virus_20',
    'torque_teno_virus_21',
    'torque_teno_virus_23',
    'torque_teno_virus_24',
    'torque_teno_virus_25',
    'torque_teno_virus_26',
    'torque_teno_virus_27',
    'torque_teno_virus_28',
    'torque_teno_virus_29',
    'torque_teno_virus_2',
    'torque_teno_virus_3',
    'torque_teno_virus_4',
    'torque_teno_virus_5',
    'torque_teno_virus_6',
    'torque_teno_virus_7',
    'torque_teno_virus_8',
    'torque_teno_virus_9',
    'torque_teno_zalophus_virus_1',
    'ttv-like_mini',
    'tuhoko_rubulavirus_1',
    'tuhoko_rubulavirus_2',
    'tuhoko_rubulavirus_3',
    'tula_orthohantavirus',
    'tupaia_paramyxovirus',
    'uganda_s',
    'uriurana',
    'urucuri',
    'usutu',
    'uukuniemi_phlebovirus',
    'vaccinia',
    'variola',
    'venezuelan_equine_encephalitis',
    'vesicular_exanthema_of_swine',
    'wesselsbron',
    'west_caucasian_bat_lyssavirus',
    'western_equine_encephalitis',
    'west_nile',
    'whataroa',
    'whitewater_arroyo_mammarenavirus',
    'wyeomyia_orthobunyavirus',
    'yaba_monkey_tumor',
    'yakeshi_orthohantavirus',
    'yaounde',
    'yellow_fever',
    'yogue',
    'yokose',
    'yug_bogdanovac_vesiculovirus',
    'zaire_ebolavirus',
    'zerdali',
    'zika',
    'zygosaccharomyces_bailii_virus_z',
]


dsc = DatasetCollection(DATASETS)

sys.modules[__name__] = dsc
