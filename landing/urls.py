from django.urls import path
import landing.views as landing

urlpatterns = [
    # path('newprojects/', landing.newprojects, name='newprojects'),
    path('projects/', landing.projects, name='projects'),
    path('projects/default/', landing.default, name='default'),
    path('projects/add/', landing.project_add, name='project_add'),
    path('projects/<id>/', landing.editor, name='editor'),
    path('projects/<id>/view/', landing.view, name='view'),
    path('projects/<id>/change/', landing.change, name='change'),
    path('projects/<id>/remove/', landing.remove, name='remove'),
    path('projects/<id>/generate/', landing.generate, name='generate'),
    path('projects/<id>/generate_more/', landing.generate_more, name='generate_more'),
    path('projects/<id>/delete/', landing.delete, name='delete'),
    path('projects/<id>/save_info/', landing.save_info, name='save_info'),
    path('projects/<id>/publish/', landing.publish, name='publish'),
    path('projects/<id>/view-site/', landing.view_site, name='view_site'),
    path('projects/<id>/generate_img/', landing.generate_img, name="generate_img"),
    path('projects/<id>/active_elements/', landing.active_elements, name="active_elements"),
    path('projects/<id>/updateData/', landing.updateData, name="updateData"),
    path('projects/<id>/updateColor/', landing.updateColor, name="updateColor"),
    path('projects/<id>/altImage/', landing.altImage, name="altImage"),
    path('projects/<id>/genMeta/', landing.genMeta, name="genMeta"),
    path('projects/<id>/updateMeta/', landing.updateMeta, name="updateMeta"),

    path('projects/<id>/new_image_gen/', landing.new_image_gen, name="new_image_gen"),
    path('projects/<id>/new_image_gen_periodic/', landing.new_image_gen_periodic, name="new_image_gen_periodic"),

    path('projects/<id>/upload_img/', landing.upload_img, name="upload_img"),
    path('projects/<id>/template_4_email/', landing.template_4_email_handler, name="template_4_email"),
    path('projects/<id>/template_2_email/', landing.template_2_email_handler, name="template_2_email"),
    path('projects/<id>/template_1_email/', landing.template_1_email_handler, name="template_1_email"),


    # new app

    path('get-started/', landing.getStarted, name='getStarted'),
    path('create/<id>', landing.create, name='create'),
    path('reGenPage/<id>', landing.reGenPage, name='reGenPage'),
    path('addMoreDetails/<id>', landing.addMoreDetails, name='addMoreDetails'),
    path('updateSecHeadOrder/<id>', landing.updateSecHeadOrder, name='updateSecHeadOrder'),
    path('updateTheme/<id>', landing.updateTheme, name='updateTheme'),
    path('theme-picker/<id>', landing.themePicker, name='themePicker'),
    path('createPage/', landing.createPage, name='createPage'),
    path('edit/<id>', landing.edit, name='edit'),
    path('promptGet/<id>', landing.promptGet, name='promptGet'),
    path('preview/<id>', landing.preview, name='preview'),
    path('respPreview/<id>', landing.respPreview, name='respPreview'),
    path('saveAllPageData/<id>', landing.saveAllPageData, name='saveAllPageData'),
    path('handlePublish/<id>', landing.handlePublish, name='handlePublish'),
    path('updateIsFirst/<id>', landing.updateIsFirst, name='updateIsFirst'),
    path('updateFavicon/<id>', landing.updateFavicon, name='updateFavicon'),
    path('all-projects/', landing.allProjects, name='allProjects'),
    path('upload_image_new', landing.upload_image_new, name='upload_image_new'),
    path('generate_new', landing.generate_new, name='generate_new'),
    path('newDelete/<id>', landing.newDelete, name='newDelete'),
    path('send_email_view/', landing.send_email_view, name='send_email_view'),

]
