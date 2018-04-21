# Maximo largo de un comentario a un posteo

commentLength = 300


# estados de prendas

checkGarmentsStatesChoices = (("toCheck","toCheck"),("accepted","accepted"),("refused","refused"))

toCheckGarmentState = checkGarmentsStatesChoices[0][0]
acceptedGarmentState = checkGarmentsStatesChoices[1][0]
refusedGarmentState =checkGarmentsStatesChoices[2][0]

# Maximo numero de posteos en "catalogo"
maxPostsOnCatalog = 10

# maximo numero de posteos (fotos probadas, prenda de compania, etc)
maxPosts = 5;

# Maximo numero de usuarios
maxUsersPerRequest = 10;

# Medidas del canvas del probador
canvasWidth = 600
canvasHeight = 450 

# Campos para serializar al UserSite
fieldsListOfCommonUsers = ["firstName","middleName","firstSurname","middleSurname"]

# Campos para serializar Company
fieldsListOfCompanies = ["name","creationDate","email","photo"]


