# Gerador de Conteúdo de Pastas

## Descrição
O **Gerador de Conteúdo de Pastas** é uma aplicação Python com interface gráfica (GUI) que permite analisar o conteúdo de uma pasta selecionada e gerar um arquivo `.txt` com a estrutura de diretórios, lista de arquivos e seus conteúdos. A ferramenta é útil para documentar projetos, criar relatórios de estruturas de pastas ou realizar auditorias de arquivos. A interface é construída com a biblioteca `tkinter` e suporta a exclusão de arquivos ou pastas específicos durante a geração do relatório.

## Funcionalidades
- Seleção de uma pasta por meio de um diálogo gráfico.
- Visualização dos arquivos e pastas do primeiro nível com tamanhos (em KB para arquivos, ou indicação de pasta).
- Opção para ignorar arquivos ou pastas específicas marcando caixas de seleção.
- Geração de um arquivo `.txt` contendo:
  - Estrutura de diretórios com caminhos relativos.
  - Lista de arquivos com seus conteúdos (se legíveis).
  - Ignora itens selecionados pelo usuário.
- Interface com rolagem para suportar pastas com muitos itens.
- Mensagens de erro e status para feedback do usuário.
- Reset automático do formulário após a geração bem-sucedida do arquivo.

## Requisitos
- **Python 3.x** instalado.
- Bibliotecas padrão do Python: `os`, `tkinter`.
- Não são necessárias bibliotecas externas adicionais.

## Como Usar
1. **Instalação**:
   - Certifique-se de que o Python está instalado. Você pode verificar executando `python --version` no terminal.
   - Baixe ou clone este repositório para o seu computador.

2. **Executando o Programa**:
   - Navegue até o diretório do projeto.
   - Execute o arquivo `start.bat` (no Windows) clicando duas vezes, ou execute manualmente no terminal:
     ```bash
     python folder_content_generator.py
     ```
   - O script `start.bat` verifica se o Python está instalado e inicia o programa.

3. **Usando a Interface**:
   - Clique em **Selecionar Pasta** para escolher a pasta que deseja analisar.
   - Uma lista de arquivos e pastas será exibida. Marque as caixas dos itens que deseja **ignorar** na geração do relatório.
   - Clique em **Gerar Arquivo .txt** para criar o relatório.
   - Escolha o local e o nome do arquivo `.txt` no diálogo de salvamento.
   - Após a geração bem-sucedida, o formulário será resetado, e uma mensagem de sucesso será exibida.

4. **Formato do Arquivo Gerado**:
   - O arquivo `.txt` contém:
     - O nome da pasta principal (prefixado com `//`).
     - Subpastas com caminhos relativos (prefixadas com `//`).
     - Arquivos com caminhos relativos, seguidos de seus conteúdos (prefixados com `// Conteúdo:`).
     - Linhas em branco entre arquivos para melhor legibilidade.
     - Erros de leitura de arquivos são registrados no relatório.

## Estrutura do Projeto
- `folder_content_generator.py`: Script principal que contém a lógica da aplicação e a interface gráfica.
- `start.bat`: Script auxiliar para verificar a instalação do Python e iniciar o programa (Windows).
- `README.md`: Este arquivo, com instruções sobre o projeto.

## Exemplo de Saída
Para uma pasta chamada `meu_projeto` com um arquivo `exemplo.txt` contendo "Olá, mundo!", o arquivo `.txt` gerado pode ser assim:
```
// meu_projeto
// meu_projeto/exemplo.txt
  // Conteúdo:
  Olá, mundo!
```

## Limitações
- A leitura de arquivos é feita com codificação `utf-8`. Arquivos em outras codificações podem gerar erros.
- Arquivos binários ou muito grandes podem causar falhas na leitura ou aumento no tempo de processamento.
- Apenas o primeiro nível de arquivos/pastas é exibido na interface para seleção de itens a ignorar.
- A aplicação não suporta arrastar e soltar pastas ou integração com linha de comando.

## Solução de Problemas
- **Erro: Python não encontrado**:
  - Instale o Python a partir de [python.org](https://www.python.org/downloads/) e adicione ao PATH do sistema.
- **Erro ao ler arquivo**:
  - Verifique se o arquivo não está bloqueado ou corrompido.
  - Arquivos binários podem não ser legíveis; considere ignorá-los.
- **Interface não exibe todos os arquivos**:
  - Use a barra de rolagem para visualizar todos os itens.
- **Nenhum arquivo gerado**:
  - Certifique-se de selecionar um local válido para salvar o arquivo no diálogo.

## Contribuições
Sinta-se à vontade para contribuir com melhorias, como:
- Suporte a outras codificações de arquivos.
- Filtros avançados para tipos de arquivos.
- Suporte a linha de comando.
- Exportação para outros formatos (ex.: JSON, Markdown).

## Licença
Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato
Para sugestões ou relatórios de bugs, crie uma issue no repositório ou entre em contato com o desenvolvedor.