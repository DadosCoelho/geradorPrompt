@echo off
title Gerador de Conteudo - Iniciando...
color 0A
echo.
echo =====================================
echo    GERADOR DE CONTEUDO DE PASTAS
echo =====================================
echo.

REM Verificar se Python está instalado
echo [INFO] Verificando instalacao do Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERRO] Python nao foi encontrado no sistema!
    echo.
    echo Para usar esta aplicacao, voce precisa instalar o Python:
    echo  1. Acesse: https://www.python.org/downloads/
    echo  2. Baixe a versao mais recente do Python
    echo  3. Durante a instalacao, marque "Add Python to PATH"
    echo  4. Reinicie o computador apos a instalacao
    echo.
    echo Pressione qualquer tecla para abrir o site do Python...
    pause >nul
    start https://www.python.org/downloads/
    goto :end
)

REM Mostrar versão do Python encontrada
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% encontrado!
echo.

REM Verificar se o arquivo principal existe
echo [INFO] Verificando arquivos da aplicacao...
if not exist "folder_content_generator.py" (
    color 0C
    echo [ERRO] Arquivo 'folder_content_generator.py' nao encontrado!
    echo.
    echo Certifique-se de que todos os arquivos estao no mesmo diretorio:
    echo  - folder_content_generator.py
    echo  - start.bat
    echo.
    goto :end
)
echo [OK] Arquivos da aplicacao encontrados!
echo.

REM Verificar dependências do tkinter
echo [INFO] Verificando interface grafica (tkinter)...
python -c "import tkinter" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0E
    echo [AVISO] Tkinter nao encontrado. Tentando instalar...
    python -m pip install tk >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [ERRO] Nao foi possivel instalar tkinter.
        echo Reinstale o Python com suporte completo a interface grafica.
        goto :end
    )
)
echo [OK] Interface grafica disponivel!
echo.

REM Iniciar aplicação
echo [INFO] Iniciando Gerador de Conteudo...
echo =====================================
echo.
title Gerador de Conteudo - Executando
color 07

python folder_content_generator.py

REM Verificar se houve erro na execução
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo =====================================
    echo [ERRO] A aplicacao foi encerrada com erro!
    echo =====================================
    echo.
    echo Possiveis causas:
    echo  - Arquivo Python com erro de sintaxe
    echo  - Falta de permissoes para executar
    echo  - Bibliotecas necessarias nao instaladas
    echo.
    echo Codigo de erro: %ERRORLEVEL%
    echo.
) else (
    echo.
    echo =====================================
    echo [INFO] Aplicacao encerrada normalmente.
    echo =====================================
    echo.
)

:end
echo Pressione qualquer tecla para fechar...
pause >nul