from landing.models import Landing, LandingImage

def get_landing_images(landing: Landing):
    images = LandingImage.objects.filter(landing=landing)
    if landing.template.template == 'template_1.html':
        result = {'t1_service_main': None}
        for image in images:
            if image.type == 'favIcon' or image.type == 't1_service_main' or (image.type and image.type.startswith('t1_service_gallery_')):
                result[image.type] = image
        return result
    if landing.template.template == 'template_2.html':
        result = {'t2_main': None, 't2_service': None}
        for image in images:
            if image.type == 'favIcon' or image.type == 't2_main' or image.type == 't2_service':
                result[image.type] = image
        return result
    if landing.template.template == 'template_3.html':
        result = {'t3_service_back': None}
        for image in images:
            if image.type == 'favIcon' or image.type == 't3_service_back' or image.type == 't3_about':
                result[image.type] = image
        return result
    if landing.template.template == 'template_4.html':
        result = {}
        for image in images:
            if image.type == 'favIcon' or image.type == 't4_main' or image.type == 't4_about' or (image.type and image.type.startswith('t4_cta_g_')) or image.type == 't4_services':
                result[image.type] = image
        return result
    return {}
