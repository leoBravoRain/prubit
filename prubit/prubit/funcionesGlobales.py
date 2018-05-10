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

# Funcion para rotar imagens si provienen de iOs (ya que por defecto se rotan en PC, pero en cellphones no aparecen rotadas)
def imageAutorotate(foto):

    with Image.open(foto) as image:
        file_format = image.format

        # Se chequea si es JPEG, ya que solo se puede extraer el exif solo desde JPEG (Usando PIL)
        if file_format == "JPEG":

            exif = image._getexif()

            # image.thumbnail((1667, 1250), resample=Image.ANTIALIAS)

            # if image has exif data about orientation, let's rotate it
            orientation_key = 274 # cf ExifTags
            if exif and orientation_key in exif:
                orientation = exif[orientation_key]

                rotate_values = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }

                if orientation in rotate_values:
                    image = image.transpose(rotate_values[orientation])

            image.save(foto.path, file_format)

            print "se rota imagen"
