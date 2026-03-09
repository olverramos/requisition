from django.db import models
from modules.auths.models import Role
import datetime 
import json

module_folder = 'modules/menu'


class Section(models.Model):
    id = models.CharField(verbose_name='ID', max_length=100, primary_key=True)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    icon = models.CharField(verbose_name='Ícono', max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/sections.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            section = Section.objects.get(pk=data["id"])
                        except Section.DoesNotExist:
                            section = Section()
                            section.id = data['id']
                            section.name = data['name']
                            if 'icon' in data.keys():
                                section.icon = data['icon']
                            section.save()                                    
                            print (f'Sección de menú {section} creada')
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'menu'
        db_table = 'menu_sections'
        ordering = ['id']
    

class Option(models.Model):
    id = models.CharField(verbose_name='ID', max_length=100, primary_key=True)
    section = models.ForeignKey('Section', verbose_name='Sección', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=100)
    url = models.CharField(verbose_name='URL', max_length=255)
    target = models.CharField(verbose_name='Nombre Pestaña', max_length=20, null=True, blank=True)
    roles = models.ManyToManyField('auths.Role', related_name='options')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/menu.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    section = None
                    if 'section' in data.keys() and data['section']:
                        section_id = data['section']
                        try:
                            section = Section.objects.get(pk=section_id)
                        except Section.DoesNotExist:
                            section = None

                    if section is not None and 'id' in data.keys() and 'title' in data.keys():
                        try:
                            option = Option.objects.get(pk=data["id"])
                        except Option.DoesNotExist:
                            option = Option()
                            option.id = data['id']
                            option.section = section
                            option.title = data['title']
                            option.url = data['url']
                            if 'target' in data.keys():
                                option.target = data['target']

                            roles = []
                            if 'roles' in data.keys():
                                for role_id in data['roles']:
                                    try:
                                        role = Role.objects.get(pk=role_id)
                                        roles.append(role)
                                    except Role.DoesNotExist:
                                        pass                                    
                            option.save()                                    
                            option.roles.set(roles)

                            print (f'Opción de menú {option} creada')

        except FileNotFoundError:
            pass

    def getDict(self):
        response = {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "target": None
        }
        if self.target:
            response['target'] = self.target

        return response

    @staticmethod
    def getMenu(account):
        section_list = Section.objects.all()
        menu_dict = {}
        for section in section_list:
            option_list = Option.objects.filter(section=section, roles=account.role)
            if option_list.count() > 0:
                section_dict = {
                    'id': section.id,
                    'name': section.name,
                    'icon': section.icon,
                    'options': [ option.getDict() for option in option_list ]
                }
        return menu_dict
    
    class Meta:
        app_label = 'menu'
        db_table = 'menu_options'
        ordering = ['id']
    