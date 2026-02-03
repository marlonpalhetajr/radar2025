#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar expediente.html, glossario.html e sumario.html
com o cabeçalho e rodapé padrão do index.html
"""

import re
import os

# Diretório do projeto
base_dir = r"c:\Users\marlon.junior\OneDrive - Fapespa\radar2024"

# Cabeçalho padrão do index.html (head + navbar)
header_template = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | FAPESPA</title>
    <meta name="description" content="{page_description}">
    <meta name="keywords" content="{page_keywords}">

    <!-- Open Graph -->
    <meta property="og:title" content="{page_title} - FAPESPA">
    <meta property="og:description" content="{page_description}">
    <meta property="og:image" content="img/anuario.png">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.fapespa.pa.gov.br/radar">

    <link rel="icon" href="img/fapespa2.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jost:wght@500;600;700&family=Open+Sans:wght@400;500&display=swap" rel="stylesheet">
    <link href="assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
    <link rel="canonical" href="https://www.fapespa.pa.gov.br/radar">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title} - FAPESPA">
    <meta name="twitter:description" content="{page_description}">
    <meta name="twitter:image" content="img/anuario.png">
    <link href="css/style.css" rel="stylesheet">
</head>

<body>
    <div id="acess-announcer" class="sr-only" aria-live="polite" aria-atomic="true"></div>

    <!-- Modal Genérico -->
    <div id="modalBackdrop" class="modal-backdrop-custom" onclick="closeCustomModal();"></div>
    <div id="contentModal" class="custom-modal">
        <div class="custom-modal-content">
            <div class="custom-modal-header">
                <h5 id="contentModalLabel">Conteúdo</h5>
                <button type="button" class="custom-modal-close" onclick="closeCustomModal();">&times;</button>
            </div>
            <div class="custom-modal-body" id="contentModalBody">
                <div class="text-center py-5">
                    <div class="spinner-border"></div>
                </div>
            </div>
            <div class="custom-modal-footer">
                <a id="modal-open-full" href="#" target="_blank" class="btn btn-outline-primary btn-sm">Abrir em nova aba</a>
                <button type="button" class="btn btn-secondary btn-sm" onclick="closeCustomModal();">Fechar</button>
            </div>
        </div>
    </div>

    <!-- Spinner Start -->
    <div id="spinner" class="show bg-white position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex align-items-center justify-content-center">
        <div class="spinner-border text-primary" role="status"></div>
    </div>
    <!-- Spinner End -->

    <!-- Navbar Start -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light sticky-top p-0" id="navbar">
        <a href="https://www.fapespa.pa.gov.br/" target="_blank" class="navbar-brand d-flex align-items-center px-4 px-lg-5">
            <h1 class="m-3">FAPESPA</h1>
        </a>
        <button type="button" class="navbar-toggler me-4" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-label="Alternar navegação">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav ms-auto p-4 p-lg-0">
                <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="index.html#radar">Radar</a></li>
                <li class="nav-item"><a class="nav-link" href="index.html#sobre">Sobre</a></li>
                <li class="nav-item"><a class="nav-link" href="index.html#contato">Contato</a></li>
                <li class="nav-item position-relative">
                    <button id="acess-open-btn" class="nav-link border-0 bg-transparent" title="Acessibilidade" onclick="toggleAccessibilityMenu(event);" type="button">
                        ♿ <span class="d-none d-lg-inline">Acessibilidade</span>
                    </button>
                    <div id="acessibilidadeMenu" class="acess-dropdown" style="display:none;">
                        <div class="acess-section-title">Visão</div>
                        <div class="acess-row">
                            <button id="acess-contrast" class="acess-control" type="button">Alto contraste</button>
                            <button id="acess-night" class="acess-control" type="button">Modo noturno</button>
                        </div>
                        <div class="acess-section-title">Cores</div>
                        <div class="acess-row">
                            <button id="acess-grayscale" class="acess-control" type="button">Escala em Cinza</button>
                        </div>
                        <div class="acess-section-title">Tamanho da Fonte</div>
                        <div class="acess-row">
                            <button id="font-dec" class="acess-control" type="button">A-</button>
                            <button id="font-reset" class="acess-control" type="button">A</button>
                            <button id="font-inc" class="acess-control" type="button">A+</button>
                        </div>
                        <div class="acess-section-title">Daltonismo</div>
                        <div class="acess-row">
                            <button id="dalton-prot" class="acess-control" type="button">Protanopia</button>
                            <button id="dalton-deut" class="acess-control" type="button">Deuteranopia</button>
                            <button id="dalton-trit" class="acess-control" type="button">Tritanopia</button>
                            <button id="dalton-off" class="acess-control" type="button">Normal</button>
                        </div>
                        <div class="acess-section-title">Leitura &amp; Legibilidade</div>
                        <div class="acess-row">
                            <button id="acess-dislexia" class="acess-control" type="button">Modo Dislexia</button>
                            <button id="acess-reading" class="acess-control" type="button">Modo Leitura</button>
                            <button id="acess-links" class="acess-control" type="button">Destacar Links</button>
                        </div>
                        <div class="acess-section-title">Movimento</div>
                        <div class="acess-row">
                            <button id="reduce-motion" class="acess-control" type="button">Reduzir Animações</button>
                        </div>
                        <div class="acess-section-title">Geral</div>
                        <div class="acess-row">
                            <button id="acess-reset" class="acess-control acess-reset" type="button">Restaurar Tudo</button>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
    <!-- Navbar End -->
'''

# Rodapé padrão do index.html
footer_template = '''
    <!-- Footer Start -->
    <div id="footer" class="container-fluid bg-dark text-light footer mt-5 py-5 wow fadeIn" data-wow-delay="0.1s">
        <div class="container py-5">
            <div class="row g-5">
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-white mb-4">Nosso Endereço</h4>
                    <p class="mb-2"><i class="fa fa-map-marker-alt me-3"></i>Av. Presidente Vargas, 670</p>
                    <p class="mb-2">Belém - PA, CEP 66017-000</p>
                    <p class="mb-2"><i class="fa fa-phone-alt me-3"></i>+55 91 3323-2550</p>
                    <p class="mb-2"><i class="fa fa-clock me-3"></i>Seg - Sex: 8h às 14h</p>
                    <p class="mb-2"><i class="fa fa-envelope me-3"></i>fapespa@fapespa.pa.gov.br</p>
                    <div class="d-flex pt-2">
                        <a class="btn btn-square btn-outline-light rounded-circle me-2" href="https://www.facebook.com/FapespaOficial" target="_blank" rel="noopener noreferrer"><i class="fab fa-facebook-f"></i></a>
                        <a class="btn btn-square btn-outline-light rounded-circle me-2" href="https://www.instagram.com/fapespa" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-white mb-4">Produtos</h4>
                    <a class="btn btn-link" href="https://www.fapespa.pa.gov.br/anuario-estatistico-do-para-2/" target="_blank">Anuário Estatístico</a>
                    <a class="btn btn-link" href="https://www.fapespa.pa.gov.br/radar-de-indicadores-das-ri/" target="_blank">Radar de Indicadores</a>
                    <a class="btn btn-link" href="https://www.fapespa.pa.gov.br/para-no-contexto-nacional-2/" target="_blank">Pará no Contexto Nacional</a>
                    <a class="btn btn-link" href="https://www.fapespa.pa.gov.br/estatistica-municipal/" target="_blank">Estatística Municipal</a>
                    <a class="btn btn-link" href="https://www.fapespa.pa.gov.br/para-em-numeros/" target="_blank">Pará em Números</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-white mb-4">Links Úteis</h4>
                    <a class="btn btn-link" href="https://www.pa.gov.br/" target="_blank">Governo do Pará</a>
                    <a class="btn btn-link" href="https://www.fapespa.pa.gov.br/" target="_blank">FAPESPA</a>
                    <a class="btn btn-link" href="politica-privacidade.html">Política de Privacidade</a>
                    <a class="btn btn-link" href="termos-uso.html">Termos de Uso</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-white mb-4">Localização</h4>
                    <p>Fundação Amazônia de Amparo a Estudos e Pesquisas</p>
                    <div class="position-relative w-100">
                        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.5362681158094!2d-48.498285788249284!3d-1.4525314985276918!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x92a48f110f9ae615%3A0xcf262f614c25afcd!2sFAPESPA%20-%20Funda%C3%A7%C3%A3o%20Amaz%C3%B4nia%20de%20Amparo%20a%20Estudos%20e%20Pesquisas!5e0!3m2!1spt-BR!2sbr!4v1698156248379!5m2!1spt-BR!2sbr" width="100%" height="150" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Footer End -->

    <!-- Copyright Start -->
    <div class="container-fluid copyright py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6 text-center text-md-start mb-3 mb-md-0">
                    &copy; <a class="border-bottom" href="https://www.fapespa.pa.gov.br/">FAPESPA</a>, Todos os direitos reservados.
                </div>
                <div class="col-md-6 text-center text-md-end">
                    Desenvolvido por <a class="border-bottom" href="https://www.fapespa.pa.gov.br/">FAPESPA</a>
                </div>
            </div>
        </div>
    </div>
    <!-- Copyright End -->

    <!-- Back to Top -->
    <a href="#" class="btn btn-lg btn-primary btn-lg-square rounded-circle back-to-top"><i class="bi bi-arrow-up"></i></a>

    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="lib/wow/wow.min.js"></script>
    <script src="lib/easing/easing.min.js"></script>
    <script src="lib/waypoints/waypoints.min.js"></script>
    <script src="lib/owlcarousel/owl.carousel.min.js"></script>
    <script src="lib/counterup/counterup.min.js"></script>
    <script src="lib/parallax/parallax.min.js"></script>
    <script src="lib/isotope/isotope.pkgd.min.js"></script>
    <script src="lib/lightbox/js/lightbox.min.js"></script>

    <!-- Template Javascript -->
    <script src="js/main.js"></script>
</body>
</html>'''

# Configurações de cada arquivo
files_config = {
    "expediente.html": {
        "title": "Expediente - Radar 2024",
        "description": "Expediente do Radar de Indicadores das Regiões de Integração do Pará",
        "keywords": "Expediente, Radar, FAPESPA, Pará"
    },
    "glossario.html": {
        "title": "Glossário - Radar 2024",
        "description": "Glossário de termos do Radar de Indicadores das Regiões de Integração",
        "keywords": "Glossário, Radar, Indicadores, FAPESPA, Termos"
    },
    "sumario.html": {
        "title": "Sumário - Radar 2024",
        "description": "Sumário do Radar de Indicadores das Regiões de Integração do Pará",
        "keywords": "Sumário, Radar, Indicadores, FAPESPA"
    }
}

def extract_main_content(file_path, filename):
    """Extrai o conteúdo principal do arquivo, removendo head, navbar e footer"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Para expediente.html - pegar conteúdo entre navbar e footer
    if filename == "expediente.html":
        # Procurar pelo conteúdo após o navbar até o footer
        match = re.search(r'<!-- Navbar End -->(.+?)<!-- Footer Start -->', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    # Para glossario.html - pegar conteúdo após navbar até footer
    elif filename == "glossario.html":
        # Procurar pelo conteúdo principal
        match = re.search(r'<!-- Navbar End -->(.+?)<!-- Footer Start -->', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    # Para sumario.html - pegar conteúdo após spinner/navbar até footer
    elif filename == "sumario.html":
        # Procurar pelo conteúdo após o navbar
        match = re.search(r'<!-- Navbar End -->(.+?)<!-- Footer Start -->', content, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Se não encontrar com esse padrão, tentar pegar após o spinner
        match = re.search(r'<!-- Spinner End -->(.+?)<!-- Footer Start -->', content, re.DOTALL)
        if match:
            # Remover navbar se existir
            main_content = match.group(1)
            main_content = re.sub(r'<!-- Navbar Start -->.*?<!-- Navbar End -->', '', main_content, flags=re.DOTALL)
            return main_content.strip()
    
    return ""

def update_file(filename):
    """Atualiza um arquivo com o template padrão"""
    file_path = os.path.join(base_dir, filename)
    
    print(f"\nProcessando {filename}...")
    
    # Extrair conteúdo principal
    main_content = extract_main_content(file_path, filename)
    
    if not main_content:
        print(f"ERRO: Não foi possível extrair o conteúdo de {filename}")
        return False
    
    # Preparar header com informações do arquivo
    config = files_config[filename]
    header = header_template.format(
        page_title=config["title"],
        page_description=config["description"],
        page_keywords=config["keywords"]
    )
    
    # Montar arquivo completo
    new_content = header + "\n\n" + main_content + "\n" + footer_template
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ {filename} atualizado com sucesso!")
    return True

def main():
    print("="*60)
    print("Atualizando arquivos com template padrão do index.html")
    print("="*60)
    
    for filename in files_config.keys():
        update_file(filename)
    
    print("\n" + "="*60)
    print("Atualização concluída!")
    print("="*60)

if __name__ == "__main__":
    main()
