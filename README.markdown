# Gerador de Conteúdo de Pastas

## Descrição
O **Gerador de Conteúdo de Pastas** é uma aplicação Python com interface gráfica (GUI) avançada que permite explorar e analisar hierarquicamente o conteúdo de uma pasta selecionada, gerando um arquivo `.txt` detalhado com a estrutura de diretórios, lista de arquivos e seus conteúdos. A ferramenta oferece controle granular sobre quais pastas e arquivos incluir no relatório, sendo ideal para documentar projetos, criar relatórios de estruturas complexas ou realizar auditorias detalhadas de arquivos.

A interface moderna é construída com `tkinter` e apresenta uma visualização em árvore hierárquica que permite navegar por toda a estrutura de pastas e subpastas, selecionando precisamente os itens desejados.

## Funcionalidades

### **Navegação e Visualização**
- **Exploração hierárquica completa**: Navegue por toda a estrutura de pastas e subpastas em uma TreeView intuitiva
- **Carregamento sob demanda**: O conteúdo das pastas é carregado apenas quando expandido, otimizando performance
- **Visualização detalhada**: Arquivos exibem tamanhos formatados (B, KB, MB, GB) e pastas são claramente identificadas
- **Scrollbars inteligentes**: Navegação fluida com barras de rolagem horizontal e vertical

### **Seleção Avançada**
- **Seleção por inclusão**: Marque os itens que deseja **incluir** no relatório (ao invés de excluir)
- **Seleção hierárquica**: Marcar uma pasta automaticamente inclui todo seu conteúdo recursivamente
- **Controle "Selecionar Tudo"**: Marque/desmarque todos os itens com um clique
- **Indicadores visuais**: ☐ (não selecionado) e ☑ (selecionado) para clareza máxima
- **Contador em tempo real**: Acompanhe quantos itens estão selecionados

### **Controles de Interface**
- **Expandir/Recolher Tudo**: Botões para expandir ou recolher toda a árvore de uma vez
- **Status informativo**: Mensagens em tempo real sobre seleções e operações
- **Interface responsiva**: Layout que se adapta ao redimensionamento da janela

### **Geração de Relatórios**
- **Arquivo .txt estruturado** contendo:
  - Estrutura completa de diretórios com caminhos relativos
  - Conteúdo completo de todos os arquivos selecionados
  - Tratamento inteligente de arquivos vazios
  - Formatação limpa e legível
- **Evita duplicatas**: Sistema inteligente que não processa o mesmo item múltiplas vezes
- **Nome sugerido**: Nome padrão baseado na pasta selecionada
- **Salvamento flexível**: Escolha local e nome do arquivo gerado

### **Tratamento de Erros**
- **Permissões**: Identifica e reporta pastas sem acesso
- **Arquivos corrompidos**: Tratamento gracioso de erros de leitura
- **Feedback claro**: Mensagens detalhadas sobre problemas encontrados

## Requisitos
- **Python 3.6+** instalado
- Bibliotecas padrão do Python: `os`, `tkinter`
- **Não são necessárias bibliotecas externas adicionais**

## Como Usar

### **1. Instalação**
- Certifique-se de que o Python está instalado executando `python --version` no terminal
- Baixe ou clone este repositório para o seu computador

### **2. Executando o Programa**
- **Windows**: Execute o arquivo `start.bat` clicando duas vezes
- **Manual**: No terminal, navegue até o diretório do projeto e execute:
  ```bash
  python folder_content_generator.py
  ```

### **3. Usando a Interface**

#### **Passo 1: Seleção da Pasta**
- Clique em **"Selecionar Pasta"** para escolher a pasta que deseja analisar
- A estrutura será carregada na árvore hierárquica

#### **Passo 2: Navegação e Exploração**
- **Expandir pastas**: Clique no triângulo ao lado das pastas para ver seu conteúdo
- **Expandir tudo**: Use o botão **"Expandir Tudo"** para ver toda a estrutura
- **Recolher**: Use **"Recolher Tudo"** para uma visão mais limpa

#### **Passo 3: Seleção de Itens**
- **Marcar itens**: Clique nos itens (☐) para marcá-los (☑)
- **Seleção hierárquica**: Marcar uma pasta inclui automaticamente todo seu conteúdo
- **Selecionar tudo**: Use a opção **"Selecionar Tudo"** para marcar todos os itens
- **Acompanhe**: O contador mostra quantos itens estão selecionados

#### **Passo 4: Geração do Relatório**
- Clique em **"Gerar Arquivo .txt"** 
- Escolha o local e nome do arquivo no diálogo de salvamento
- Aguarde a confirmação de sucesso

### **4. Interpretando o Arquivo Gerado**
O arquivo `.txt` contém:
- **Pastas**: Listadas com `/` no final (ex: `// minha_pasta/`)
- **Arquivos**: Seguidos de seu conteúdo completo
- **Estrutura**: Caminhos relativos organizados hierarquicamente
- **Conteúdo**: Precedido por `// Conteúdo:` e com indentação
- **Erros**: Reportados quando arquivos não podem ser lidos

## Exemplo de Saída
Para uma pasta `meu_projeto` com estrutura:
```
meu_projeto/
├── README.md
├── src/
│   ├── main.py
│   └── utils.py
└── docs/
    └── manual.txt
```

O arquivo gerado seria:
```
// meu_projeto/
// meu_projeto/README.md
  // Conteúdo:
  # Meu Projeto
  Este é um projeto exemplo.

// meu_projeto/src/
// meu_projeto/src/main.py
  // Conteúdo:
  print("Hello World!")

// meu_projeto/src/utils.py
  // Conteúdo:
  def helper_function():
      return "Helper"

// meu_projeto/docs/
// meu_projeto/docs/manual.txt
  // Conteúdo:
  Manual do usuário...
```

## Estrutura do Projeto
- `folder_content_generator.py`: Script principal com interface gráfica e lógica da aplicação
- `start.bat`: Script auxiliar para Windows (verifica Python e inicia o programa)
- `README.markdown`: Este arquivo com instruções detalhadas
- `icon.ico`: Ícone opcional usado pela aplicação
- `LICENSE.txt`: Arquivo de licença (MIT)

## Vantagens da Nova Versão

### **Controle Granular**
- Selecione exatamente o que quer incluir no relatório
- Navegue por estruturas complexas com facilidade
- Evite processar arquivos grandes desnecessários

### **Performance Otimizada**
- Carregamento sob demanda economiza memória
- Sistema anti-duplicata evita processamento redundante
- Interface responsiva mesmo com muitos arquivos

### **Usabilidade Aprimorada**
- Interface intuitiva com indicadores visuais claros
- Controles rápidos para operações comuns
- Feedback constante sobre ações do usuário

## Limitações
- **Codificação**: Leitura de arquivos feita em UTF-8 (arquivos em outras codificações podem gerar erros)
- **Arquivos binários**: Podem causar erros na leitura (são reportados no arquivo gerado)
- **Permissões**: Pastas sem acesso são identificadas mas não processadas
- **Performance**: Estruturas muito grandes podem demorar para carregar completamente

## Solução de Problemas

### **Problemas de Instalação**
- **"Python não encontrado"**: 
  - Instale Python de [python.org](https://www.python.org/downloads/)
  - Adicione Python ao PATH do sistema

### **Problemas de Interface**
- **Árvore não carrega**: Verifique permissões da pasta selecionada
- **Interface lenta**: Use "Recolher Tudo" e expanda apenas o necessário
- **Itens não aparecem**: Use as scrollbars para navegar

### **Problemas de Geração**
- **"Nenhum item selecionado"**: Marque pelo menos um arquivo ou pasta
- **Arquivo não gerado**: Verifique permissões de escrita no local escolhido
- **Erro de leitura**: Alguns arquivos podem estar bloqueados ou corrompidos

## Dicas de Uso

### **Para Projetos Grandes**
1. Use "Expandir Tudo" apenas quando necessário
2. Selecione pastas específicas ao invés de "Selecionar Tudo"
3. Exclua pastas de cache/build desmarcando-as

### **Para Documentação**
1. Inclua apenas arquivos de código e documentação
2. Use a visualização hierárquica para entender a estrutura
3. O arquivo gerado serve como snapshot completo do projeto

### **Para Auditoria**
1. Expanda toda a estrutura para ver todos os arquivos
2. Use "Selecionar Tudo" para relatório completo
3. Analise erros reportados para identificar problemas

## Contribuições
Contribuições são bem-vindas! Ideias para melhorias:
- **Filtros avançados**: Por tipo de arquivo, tamanho, data
- **Formatos de exportação**: JSON, XML, HTML, Markdown
- **Interface de linha de comando**: Para automação
- **Suporte a mais codificações**: Detecção automática de encoding
- **Visualização em tempo real**: Preview do conteúdo antes da geração
- **Compressão**: Geração de arquivos ZIP com relatórios

## Licença
Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Histórico de Versões

### **Versão 2.0 (Atual)**
- ✅ Interface hierárquica com TreeView
- ✅ Navegação completa por subpastas
- ✅ Seleção por inclusão (ao invés de exclusão)
- ✅ Controles "Selecionar Tudo", "Expandir Tudo", "Recolher Tudo"
- ✅ Contador de itens selecionados
- ✅ Carregamento sob demanda para performance
- ✅ Interface moderna e responsiva
- ✅ Tratamento aprimorado de erros

### **Versão 1.0**
- Interface básica com lista simples
- Seleção por exclusão apenas
- Limitado ao primeiro nível de pastas

## Contato
Para sugestões, relatórios de bugs ou contribuições:
- Crie uma issue no repositório
- Entre em contato com o desenvolvedor
- Contribua com pull requests

---

**Desenvolvido com ❤️ para facilitar a documentação e análise de estruturas de pastas complexas.**