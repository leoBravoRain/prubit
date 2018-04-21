# -*- coding: utf-8 -*-

# Usado por el metodo resizePhoto
import PIL
from PIL import Image

# Metodo para hacer resize de imagen
def resizePhoto(self, maxWidth, maxHeight, Garment, GarmentsToCheck):

	# Se toman todas las imagenes de la prenda

	# Se crea lista de fotos
	# valor inicial es la foto principal 
	photosNamesList = ["photo"];

	# Si es que tiene foto secundaria

	# Si es que es una prenda
	if isinstance(self,GarmentsToCheck) and isinstance(self,Garment):

		if self.secondaryPhoto:

			# Se agrega el nombre de la foto secundaria
			photosNamesList.append("secondaryPhoto")

	# Se itera sobre cada nombre de foto

	for photoName in photosNamesList:

		# Se toma la imagen
		if photoName == "photo":

			image = Image.open(self.photo)

		elif photoName == "secondaryPhoto":

			image = Image.open(self.secondaryPhoto)

		# Se toma el tamaño de la imagen
		(width, height) = image.size

		# Se inicia el resize de la imagen

		# Si es qeu el ancho de la imagen es mayor que el maximo 
		if width > maxWidth:

			# Se calcula el nuevo alto que deberia tener manteniendo la proporcion de la imagen original. la proporcion es: ancho viejo / alto viejo = ancho nuevo / alto nuevo
			razonAnchos = (maxWidth/float(image.size[0]))
			nuevoAlto = int((float(image.size[1])*float(razonAnchos)))

			# Se aplica resize de la imagen
			image = image.resize((maxWidth,nuevoAlto), Image.ANTIALIAS)

			# Si es que el alto es mayor al maximo
			if image.size[1] > maxHeight:

				# Se calcula el nuevo anho que deberia tener manteniendo la proporcion de la imagen original. la proporcion es: ancho viejo / alto viejo = ancho nuevo / alto nuevo
				hpercent = (maxHeight/float(image.size[1]))
				wsize = int((float(image.size[0])*float(hpercent)))

				# Se aplica resize de la imagen
				image = image.resize((wsize,maxHeight), Image.ANTIALIAS)

		# Si es que el alto es mayor al maximo
		elif image.size[1] > maxHeight:

			# Se calcula el nuevo ancho que deberia tener manteniendo la proporcion de la imagen original. la proporcion es: ancho viejo / alto viejo = ancho nuevo / alto nuevo
			hpercent = (maxHeight/float(image.size[1]))
			wsize = int((float(image.size[0])*float(hpercent)))

			# Se aplica resize de la imagen
			image = image.resize((wsize,maxHeight), Image.ANTIALIAS)

			# Si es que el ancho es mayor al maximo
			if image.size[0] > maxWidth:

				# Se calcula el nuevo alto que deberia tener manteniendo la proporcion de la imagen original. la proporcion es: ancho viejo / alto viejo = ancho nuevo / alto nuevo
				razonAncho = (maxWidth/float(image.size[0]))
				nuevoAlto = int((float(image.size[1])*float(razonAncho)))

				# Se aplica resize a la imagen
				image = image.resize((maxWidth,nuevoAlto), Image.ANTIALIAS)		

		# Se guarda finalmente la imagen con resize
		if photoName == "photo":

			image.save(self.photo.path)

		elif photoName == "secondaryPhoto":

			image.save(self.secondaryPhoto.path)


