@echo off
echo Verificando instalacao do Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erro: Python nao encontrado. Por favor, instale o Python e tente novamente.
    echo Voce pode baixar o Python em https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Iniciando o programa...
python folder_content_generator.py
if %ERRORLEVEL% NEQ 0 (
    echo Erro ao executar o programa. Verifique se o arquivo folder_content_generator.py existe e se voce tem permissoes para executa-lo.
    pause
    exit /b 1
)

pause