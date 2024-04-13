# Função generate_images
# recebe o prompt do usuario
# joga na api do chatgpt -> a gente pode tentar depois ver a diferença de execução pra algum modelo do huggingface
#! estudar o repositório infinite-zoom-automatic1111-webui para entender como ele fez a função de geração de imagens
# pega a resposta, joga na função do stable diffusion -> função do stable diffusion guarda as imagens em uma pasta 
# (guarda no banco de dados)
# pegas as imagens geradas na pasta e retorna para o front-end 

# Função get_existent_images
# recebe o id do projeto 
# busca no banco de dados as imagens geradas para o projeto
# retorna as imagens para o front-end
