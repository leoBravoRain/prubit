# -*- coding: utf-8 -*-
from django import forms
from usuarios.models import Company_TradeMark,GENDER_CHOICE
from prendas.models import GarmentType
import datetime



class EditGarmentRefusedForm(forms.Form):

	def __init__(self,*args,**kwargs):
		garment = kwargs.pop("garment")
		super(EditGarmentRefusedForm,self).__init__(*args,**kwargs)
		self.fields["name"]= forms.CharField(required = False, initial=garment.name)
		self.fields["price"]= forms.CharField(required = False, initial=garment.price)		
		self.fields["photo"]= forms.ImageField(required = False)
		self.fields["photo"].widget.attrs.update({
			'class': "image"
			}) #override class to "image" because this is used by the picedit.js
		self.fields["observation"]= forms.CharField(required = False, initial=garment.observation)
		self.fields["type1"]= forms.ModelChoiceField(required=False,queryset=GarmentType.objects.all(), initial=garment.type1)
		self.fields["gender"]= forms.ChoiceField(choices=GENDER_CHOICE,required=False, initial = garment.gender)
		self.fields["size"]= forms.CharField(required = False, initial=garment.size)
		trademarks = Company_TradeMark.objects.filter(company__id__exact=garment.company_trademark.company.id).values_list("tradeMark__name",flat=True)
		trademarksList = []
		choices = [(trademarks[i],trademarks[i]) for i in range(0,len(trademarks))]
		self.fields["tradeMark"]= forms.ChoiceField(choices=choices, initial = garment.company_trademark.tradeMark)
		self.fields["dimensions"]= forms.CharField(required = False, initial=garment.dimensions)
		self.fields["linkToBuyOnCompanySite"]= forms.CharField(required = False, initial=garment.linkToBuyOnCompanySite)

class EditGarmentToCheckForm(forms.Form):
	# photo = forms.ImageField(required = False)
	def __init__(self,*args,**kwargs):
		garment = kwargs.pop("garment")
		super(EditGarmentToCheckForm,self).__init__(*args,**kwargs)
		self.fields["name"]= forms.CharField(required = False, initial=garment.name)
		self.fields["price"]= forms.CharField(required = False, initial=garment.price)		
		self.fields["photo"]= forms.ImageField(required = False)
		self.fields["photo"].widget.attrs.update({
			'class': "image"
			}) #override class to "image" because this is used by the picedit.js
		self.fields["observation"]= forms.CharField(required = False, initial=garment.observation)
		self.fields["type1"]= forms.ModelChoiceField(required=False,queryset=GarmentType.objects.all(), initial=garment.type1)
		self.fields["gender"]= forms.ChoiceField(choices=GENDER_CHOICE,required=False, initial = garment.gender)
		self.fields["size"]= forms.CharField(required = False, initial=garment.size)
		trademarks = Company_TradeMark.objects.filter(company__id__exact=garment.company_trademark.company.id).values_list("tradeMark__name",flat=True)
		trademarksList = []
		choices = [(trademarks[i],trademarks[i]) for i in range(0,len(trademarks))]
		self.fields["tradeMark"]= forms.ChoiceField(choices=choices, initial = garment.company_trademark.tradeMark)
		self.fields["dimensions"]= forms.CharField(required = False, initial=garment.dimensions)
		self.fields["linkToBuyOnCompanySite"]= forms.CharField(required = False, initial=garment.linkToBuyOnCompanySite)
		
class EditGarmentForm(forms.Form):
	def __init__(self,*args,**kwargs):
		garment = kwargs.pop("garment")
		super(EditGarmentForm,self).__init__(*args,**kwargs)
		self.fields["name"]= forms.CharField(required = False, initial=garment.name)
		self.fields["price"]= forms.CharField(required = False, initial=garment.price)		
		# self.fields["photo"]= forms.ImageField(required = False, initial=garment.photo)
		self.fields["observation"]= forms.CharField(required = False, initial=garment.observation)
		self.fields["type1"]= forms.ModelChoiceField(required=False,queryset=GarmentType.objects.all(), initial=garment.type1)
		self.fields["gender"]= forms.ChoiceField(choices=GENDER_CHOICE,required=False, initial = garment.gender)
		self.fields["size"]= forms.CharField(required = False, initial=garment.size)
		trademarks = Company_TradeMark.objects.filter(company__id__exact=garment.company_trademark.company.id).values_list("tradeMark__name",flat=True)
		trademarksList = []
		choices = [(trademarks[i],trademarks[i]) for i in range(0,len(trademarks))]
		self.fields["tradeMark"]= forms.ChoiceField(choices=choices, initial = garment.company_trademark.tradeMark)
		self.fields["dimensions"]= forms.CharField(required = False, initial=garment.dimensions)
		self.fields["linkToBuyOnCompanySite"]= forms.CharField(required = False, initial=garment.linkToBuyOnCompanySite)



#This has the same definition in models.py Garment
class AddPhotoGarmentForm(forms.Form):

	name = forms.CharField(required=False,initial="BORRAR")
	price = forms.DecimalField(help_text="19,99",required=False,initial=9)

	# Foto principal
	photo = forms.ImageField(required=True,label="Foto", error_messages={'required': "Por favor, agregue una imagen"})

	# Foto principal
	secondaryPhoto = forms.ImageField(required=False,label="Foto secundaria",help_text="Ponga una foto de la prenda en otra posicion")

	observation = forms.CharField(required=False)

	# Se toman los tipos de prenads
	initialGarmentType = GarmentType.objects.all()

	# Si es qeu existe al menos 1 tipo de prenda
	# if initialGarmentType:

	# 	initialGarmentType = initialGarmentType[0]
		
	# # Si es que no existe ningun tipo se retorna lista vacia
	# else:
	# 	initialGarmentType = []

	# type1 = forms.ModelChoiceField(required=False,queryset = GarmentType.objects.all().values_list("type1",flat=True), initial=initialGarmentType)
	type1 = forms.ModelChoiceField(required=False,queryset = GarmentType.objects.all(), initial=initialGarmentType)

	gender = forms.ChoiceField(choices=GENDER_CHOICE,required=False)

	size = forms.CharField(help_text="max 2",required=False)
	dimensions = forms.CharField(required=False)
	# Link para dirigir a sitio de compra de la compañia
	linkToBuyOnCompanySite = forms.CharField(required=False,max_length = 1000,initial="www.pruvit.com (Borrar parte que dice 'http://')",help_text="No colocar http://",label="Link para que cliente pueda comprar la prenda")
	# Se obtiene Id para seleccionar las marcas de la compania
	def __init__(self,*args,**kwargs):
		myCompany = kwargs.pop("meId")
		trademarks = Company_TradeMark.objects.filter(company__id__exact=myCompany).values_list("tradeMark__name",flat=True)
		trademarksList = []
		choices = [(trademarks[i],trademarks[i]) for i in range(0,len(trademarks))]
		super(AddPhotoGarmentForm,self).__init__(*args,**kwargs)
		self.fields["tradeMark"]=forms.ChoiceField(choices=choices)
		# self.fields["photo"].widget.attrs.update({
		# 	'class': "image"
		# 	}) #override class to "image" because this is used by the picedit.js
		# se agregan para darle formato con bootstrap
		self.fields["name"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["price"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["observation"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["type1"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["gender"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["size"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["dimensions"].widget.attrs.update({
			'class': "form-control"
			})
		self.fields["linkToBuyOnCompanySite"].widget.attrs.update({
			'class':"form-control"
			})