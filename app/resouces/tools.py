from time import sleep
import numpy as np
from cv2 import resize

def process_image(img):
    img = resize(img, (224, 224))
    img = img.reshape(1, 224, 224, 3)
    #img = preprocess_input(img)
    return img


def predict(img, model):
    classn = ['acura_tl_2003', 'acura_tl_2006', 'audi_a4_2004', 'audi_a4_2006', 'bmw_325i_2003', 'bmw_x5_2001', 'cadillac_cts_2005', 'cadillac_cts_2006', 'chevrolet_impala_2007', 'chevrolet_silverado_1999', 'chrysler_pacifica_2004', 'chrysler_pacifica_2006', 'dodge_avenger_2008', 'dodge_durango_1998', 'ford_f150_2010', 'ford_f250_1999', 'gmc_envoy_2003', 'honda_civic_2002', 'honda_civic_2009', 'hyundai_elantra_2002', 'hyundai_elantra_2005', 'infiniti_g35_2004', 'infiniti_g35_coupe_2004', 'jeep_grand_cherokee_1997', 'jeep_liberty_2006', 'kia_sedona_2005', 'kia_sorento_2005', 'lexus_is300_2002',
              'lexus_rx300_1999', 'lincoln_ls_2002', 'lincoln_navigator_2003', 'mazda_6_2005', 'mazda_rx8_2004', 'mercury_mountaineer_2002', 'mercury_mountaineer_2004', 'mini_cooper_2003', 'mini_cooper_2006', 'mitsubishi_eclipse_2001', 'mitsubishi_lancer_2003', 'nissan_altima_2002', 'nissan_altima_2003', 'nissan_sentra_2006', 'pontiac_g6_2007', 'pontiac_g6_2008', 'saturn_ion_2004', 'saturn_vue_2003', 'scion_tc_2007', 'scion_tc_2008', 'subaru_outback_2001', 'subaru_outback_2003', 'toyota_camry_2002', 'toyota_camry_2007', 'volkswagen_jetta_2003', 'volkswagen_jetta_2006', 'volvo_s60_2002', 'volvo_xc90_2004']
    predictions = model.predict(img)
    label = classn[predictions.argmax()]
    probability_Value = np.amax(predictions)
    if probability_Value > 0.6:
        car_model = label  # mazda_6_2005_22
        car_brand = label.split('_')[0]  # mazda

        result = {
            'brand': car_brand,
            'model': car_model
        }
        return result,probability_Value

    return {
        'brand': 'unknown',
        'model': 'unknown'
    },None
