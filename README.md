Criação do Usuário Administrador:

Inicialmente, é fundamental criar um usuário administrador.
Para isso, utilize o terminal e execute o seguinte comando:

Copiar código
python manage.py createsuperuser

vamos também migrar todos dados adicionais para o site utilize:

Copiar Código

python manage.py makemigrations

depois

python manage.py migrate


Siga as instruções fornecidas para concluir a criação do super usuário.


Atribuição de Privilégios Administrativos:

Após a criação do super usuário, é necessário atribuir-lhe funções administrativas.
Primeiramente, crie uma conta na página designada para este fim.
Configuração de Permissões Administrativas:




Após criar a conta, acesse a área administrativa (/admin) do sistema.
Dentro desta área, adicione as permissões administrativas ao usuário em questão.
Com as permissões concedidas, o usuário será capaz de gerenciar as anotações conforme necessário.

Feito isso utilize o comando:

python manage.py runserver

