import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

####################### CERTIFICADOS AVALIADORES ########################

# Caminho para o arquivo da fonte
font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-SemiBold.ttf"
pdfmetrics.registerFont(TTFont("Poppins", font_path))

# Caminhos completos para os arquivos
modelo_av_path = '/home/leticia/Downloads/Emissor de certificado automático/modelo_av.pdf'
avaliadores_path = '/home/leticia/Downloads/Emissor de certificado automático/avaliadores.txt'

def draw_centered_text(c, text, y_position, width, font_name, font_size):
    text_width = c.stringWidth(text, font_name, font_size)
    x_position = (width - text_width) / 2  
    
    c.drawString(x_position, y_position, text)

def add_name_to_certificate(pdf_path, output_path, name):
    print(f"Processando o nome: {name}")

    custom_size = (29.70 * cm, 21.00 * cm)  # Define o tamanho customizado

    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=custom_size)  # Usa o tamanho customizado
        width, height = custom_size  # Usa o tamanho customizado

        font_size = 22
        c.setFont("Poppins", font_size)
        c.setFillColorRGB(0.2, 0.2, 0.5)  # Azul escuro acinzentado
        #c.setFillColorRGB(0.07, 0.04, 0.56)

        if c.stringWidth(name, "Poppins", font_size) > width - 50:
            parts = name.split(' ')
            halfway = len(parts) // 2
            name_line_1 = ' '.join(parts[:halfway])
            name_line_2 = ' '.join(parts[halfway:])
            
            draw_centered_text(c, name_line_1, height/2 + font_size/3 - 30, width, "Poppins", font_size)
            draw_centered_text(c, name_line_2, height/2 - font_size/2 - 38, width, "Poppins", font_size)
        else:
            draw_centered_text(c, name, height/2 - 35, width, "Poppins", font_size)  

        c.save()

        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    print(f"Certificado para {name} concluído!")

def main():
    with open(avaliadores_path, 'r', encoding='utf-8-sig') as f:
        names = f.readlines()

        for name in names:
            cleaned_name = name.strip()

            output_path = f"/home/leticia/Downloads/Emissor de certificado automático/certificados_avaliadores/certificado_avaliador(a)_{cleaned_name}.pdf"
            
            add_name_to_certificate(modelo_av_path, output_path, cleaned_name)
            print(f"Certificado gerado para {cleaned_name} em {output_path}")

if __name__ == '__main__':
    main()

####################### CERTIFICADOS PALESTRANTES ########################


# Caminho para o arquivo da fonte
font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-SemiBold.ttf"
pdfmetrics.registerFont(TTFont("Poppins", font_path))

bold_font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-Bold.ttf"  
pdfmetrics.registerFont(TTFont("Poppins-Bold", bold_font_path))


# Caminhos completos para os arquivos
modelo_palestrante_path = '/home/leticia/Downloads/Emissor de certificado automático/modelo_palestrante.pdf'
palestrantes_path = '/home/leticia/Downloads/Emissor de certificado automático/palestrantes.txt'


def draw_title_text(c, title, y_position, width, font_name, font_size, max_title_width):
    words = title.split(' ')
    lines = []
    current_line = []

    # Constrói as linhas baseado na largura máxima
    for word in words:
        if c.stringWidth(' '.join(current_line + [word]), font_name, font_size) <= max_title_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    # Desenhando o título centralizado linha por linha
    for i, line in enumerate(lines):
        draw_centered_text(c, line, y_position - i*(font_size + 5), width, font_name, font_size)


def draw_centered_text(c, text, y_position, width, font_name, font_size):
    text_width = c.stringWidth(text, font_name, font_size)
    x_position = (width - text_width) / 2  
    
    c.drawString(x_position, y_position, text)

def add_name_to_certificate(pdf_path, output_path, name, title):
    print(f"Processando o nome: {name}")

    custom_size = (29.70 * cm, 21.00 * cm)  # Define o tamanho customizado

    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=custom_size)  #  tamanho customizado
        width, height = custom_size  #  tamanho customizado

        # Colocando o título.
        font_size_title = 16
        c.setFont("Poppins-Bold", font_size_title)
        max_title_width = 23 * cm
        c.setFillColorRGB(0.07, 0.08, 0.3) # Azul escuro 
        draw_title_text(c, title, height/2 - 30, width, "Poppins-Bold", font_size_title, max_title_width)

        font_size = 22
        c.setFont("Poppins", font_size)
        c.setFillColorRGB(0.2, 0.2, 0.5)  # Azul médio acinzentado
        #c.setFillColorRGB(0.07, 0.04, 0.56)

        if c.stringWidth(name, "Poppins", font_size) > width - 50:
            parts = name.split(' ')
            halfway = len(parts) // 2
            name_line_1 = ' '.join(parts[:halfway])
            name_line_2 = ' '.join(parts[halfway:])
            
            draw_centered_text(c, name_line_1, height/2 + font_size/3 - 30, width, "Poppins", font_size)
            draw_centered_text(c, name_line_2, height/2 - font_size/2 - 38, width, "Poppins", font_size)
        else:
            draw_centered_text(c, name, height/2 + 20, width, "Poppins", font_size)  

        c.save()

        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    print(f"Certificado para {name} concluído!")

def main():
  with open(palestrantes_path, 'r', encoding='utf-8-sig') as f_names, \
         open('/home/leticia/Downloads/Emissor de certificado automático/titulos_palestras.txt', 'r', encoding='utf-8-sig') as f_titles:
        
        names = f_names.readlines()
        titles = f_titles.readlines()

        for name, title in zip(names, titles):
            cleaned_name = name.strip()
            cleaned_title = title.strip()

            output_path = f"/home/leticia/Downloads/Emissor de certificado automático/certificados_palestrantes/certificado_palestrante_{cleaned_name}.pdf"
            
            add_name_to_certificate(modelo_palestrante_path, output_path, cleaned_name, cleaned_title)
            print(f"Certificado gerado para {cleaned_name} em {output_path}")


if __name__ == '__main__':
    main()

####################### CERTIFICADOS APRESENTAÇÕES DE BANNERS ########################


# Caminho para o arquivo da fonte
font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-SemiBold.ttf"
pdfmetrics.registerFont(TTFont("Poppins", font_path))

bold_font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-Bold.ttf"  
pdfmetrics.registerFont(TTFont("Poppins-Bold", bold_font_path))


# Caminhos completos para os arquivos
modelo_banner_path = '/home/leticia/Downloads/Emissor de certificado automático/modelo_banner.pdf'
banners_path = '/home/leticia/Downloads/Emissor de certificado automático/banners.txt'


def draw_title_text(c, title, y_position, width, font_name, font_size, max_title_width):
    words = title.split(' ')
    lines = []
    current_line = []

    # Constrói as linhas baseado na largura máxima
    for word in words:
        if c.stringWidth(' '.join(current_line + [word]), font_name, font_size) <= max_title_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    # Desenhando o título centralizado linha por linha
    for i, line in enumerate(lines):
        draw_centered_text(c, line, y_position - i*(font_size + 5), width, font_name, font_size)


def draw_centered_text(c, text, y_position, width, font_name, font_size):
    text_width = c.stringWidth(text, font_name, font_size)
    x_position = (width - text_width) / 2  
    
    c.drawString(x_position, y_position, text)

def add_name_to_certificate(pdf_path, output_path, name, title):
    print(f"Processando o nome: {name}")

    custom_size = (29.70 * cm, 21.00 * cm)  # Define o tamanho customizado

    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=custom_size)  #  tamanho customizado
        width, height = custom_size  #  tamanho customizado

        # Colocando o título.
        font_size_title = 16
        c.setFont("Poppins-Bold", font_size_title)
        max_title_width = 23 * cm
        c.setFillColorRGB(0.07, 0.08, 0.3) # Azul escuro 
        draw_title_text(c, title, height/2 - 30, width, "Poppins-Bold", font_size_title, max_title_width)

        font_size = 22
        c.setFont("Poppins", font_size)
        c.setFillColorRGB(0.2, 0.2, 0.5)  # Azul médio acinzentado
        #c.setFillColorRGB(0.07, 0.04, 0.56)

        if c.stringWidth(name, "Poppins", font_size) > width - 50:
            parts = name.split(' ')
            halfway = len(parts) // 2
            name_line_1 = ' '.join(parts[:halfway])
            name_line_2 = ' '.join(parts[halfway:])
            
            draw_centered_text(c, name_line_1, height/2 + font_size/3 - 30, width, "Poppins", font_size)
            draw_centered_text(c, name_line_2, height/2 - font_size/2 - 38, width, "Poppins", font_size)
        else:
            draw_centered_text(c, name, height/2 + 20, width, "Poppins", font_size)  

        c.save()

        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    print(f"Certificado para {name} concluído!")

def main():
  with open(banners_path, 'r', encoding='utf-8-sig') as f_names, \
         open('/home/leticia/Downloads/Emissor de certificado automático/titulos_banners.txt', 'r', encoding='utf-8-sig') as f_titles:
        
        names = f_names.readlines()
        titles = f_titles.readlines()

        for name, title in zip(names, titles):
            cleaned_name = name.strip()
            cleaned_title = title.strip()

            output_path = f"/home/leticia/Downloads/Emissor de certificado automático/certificados_apresentadores_banners/certificado_apresentador(a)_de_banner_{cleaned_name}.pdf"
            
            add_name_to_certificate(modelo_banner_path, output_path, cleaned_name, cleaned_title)
            print(f"Certificado gerado para {cleaned_name} em {output_path}")


if __name__ == '__main__':
    main()

####################### CERTIFICADOS PARTICIPAÇÃO NO EVENTO ########################


# Caminho para o arquivo da fonte
font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-SemiBold.ttf"
pdfmetrics.registerFont(TTFont("Poppins", font_path))

# Caminhos completos para os arquivos
modelo_participacao_path = '/home/leticia/Downloads/Emissor de certificado automático/modelo_participacao.pdf'
participantes_path = '/home/leticia/Downloads/Emissor de certificado automático/participantes.txt'

def draw_centered_text(c, text, y_position, width, font_name, font_size):
    text_width = c.stringWidth(text, font_name, font_size)
    x_position = (width - text_width) / 2  + 65
    
    c.drawString(x_position, y_position, text)

def add_name_to_certificate(pdf_path, output_path, name):
    print(f"Processando o nome: {name}")

    custom_size = (29.70 * cm, 21.00 * cm)  # Define o tamanho customizado

    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=custom_size)  # Usa o tamanho customizado
        width, height = custom_size  # Usa o tamanho customizado

        font_size = 16
        c.setFont("Poppins", font_size)
        c.setFillColorRGB(0.2, 0.2, 0.5)  # Azul escuro acinzentado
        #c.setFillColorRGB(0.07, 0.04, 0.56)

        if c.stringWidth(name, "Poppins", font_size) > width - 50:
            parts = name.split(' ')
            halfway = len(parts) // 2
            name_line_1 = ' '.join(parts[:halfway])
            name_line_2 = ' '.join(parts[halfway:])
            
            draw_centered_text(c, name_line_1, height/2 + font_size/3 - 30, width, "Poppins", font_size)
            draw_centered_text(c, name_line_2, height/2 - font_size/2 - 38, width, "Poppins", font_size)
        else:
            draw_centered_text(c, name, height/2 - 21, width, "Poppins", font_size)  

        c.save()

        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    print(f"Certificado para {name} concluído!")

def main():
    with open(participantes_path, 'r', encoding='utf-8-sig') as f:
        names = f.readlines()

        for name in names:
            cleaned_name = name.strip()

            output_path = f"/home/leticia/Downloads/Emissor de certificado automático/certificados_de_participação/certificado_participante_{cleaned_name}.pdf"
            
            add_name_to_certificate(modelo_participacao_path, output_path, cleaned_name)
            print(f"Certificado gerado para {cleaned_name} em {output_path}")

if __name__ == '__main__':
    main()


####################### CERTIFICADOS ORGANIZAÇÃOS ########################

# Caminho para o arquivo da fonte
font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-SemiBold.ttf"
pdfmetrics.registerFont(TTFont("Poppins", font_path))

# Caminhos completos para os arquivos
modelo_organizacao_path = '/home/leticia/Downloads/Emissor de certificado automático/modelo_organizacao.pdf'
organizacao_path = '/home/leticia/Downloads/Emissor de certificado automático/organizacao.txt'

def draw_centered_text(c, text, y_position, width, font_name, font_size):
    text_width = c.stringWidth(text, font_name, font_size)
    x_position = (width - text_width) / 2  
    
    c.drawString(x_position, y_position, text)

def add_name_to_certificate(pdf_path, output_path, name):
    print(f"Processando o nome: {name}")

    custom_size = (29.70 * cm, 21.00 * cm)  # Define o tamanho customizado

    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=custom_size)  # Usa o tamanho customizado
        width, height = custom_size  # Usa o tamanho customizado

        font_size = 22
        c.setFont("Poppins", font_size)
        c.setFillColorRGB(0.2, 0.2, 0.5)  # Azul escuro acinzentado
        #c.setFillColorRGB(0.07, 0.04, 0.56)

        if c.stringWidth(name, "Poppins", font_size) > width - 50:
            parts = name.split(' ')
            halfway = len(parts) // 2
            name_line_1 = ' '.join(parts[:halfway])
            name_line_2 = ' '.join(parts[halfway:])
            
            draw_centered_text(c, name_line_1, height/2 + font_size/3 - 30, width, "Poppins", font_size)
            draw_centered_text(c, name_line_2, height/2 - font_size/2 - 38, width, "Poppins", font_size)
        else:
            draw_centered_text(c, name, height/2 - 35, width, "Poppins", font_size)  

        c.save()

        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    print(f"Certificado para {name} concluído!")

def main():
    with open(organizacao_path, 'r', encoding='utf-8-sig') as f:
        names = f.readlines()

        for name in names:
            cleaned_name = name.strip()

            output_path = f"/home/leticia/Downloads/Emissor de certificado automático/certificados_organizacao/certificado_organizador(a)_{cleaned_name}.pdf"
            
            add_name_to_certificate(modelo_organizacao_path, output_path, cleaned_name)
            print(f"Certificado gerado para {cleaned_name} em {output_path}")

if __name__ == '__main__':
    main()

####################### CERTIFICADOS APRESENTAÇÕES ORAIS ########################


# Caminho para o arquivo da fonte
font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-SemiBold.ttf"
pdfmetrics.registerFont(TTFont("Poppins", font_path))


bold_font_path = "/home/leticia/Downloads/Emissor de certificado automático/Poppins-Bold.ttf" 
pdfmetrics.registerFont(TTFont("Poppins-Bold", bold_font_path))




# Caminhos completos para os arquivos
modelo_ap_oral_path = '/home/leticia/Downloads/Emissor de certificado automático/modelo_ap_oral.pdf'
ap_orais_path = '/home/leticia/Downloads/Emissor de certificado automático/ap_orais.txt'




def draw_title_text(c, title, y_position, width, font_name, font_size, max_title_width):
   words = title.split(' ')
   lines = []
   current_line = []


   # Constrói as linhas baseado na largura máxima
   for word in words:
       if c.stringWidth(' '.join(current_line + [word]), font_name, font_size) <= max_title_width:
           current_line.append(word)
       else:
           lines.append(' '.join(current_line))
           current_line = [word]


   if current_line:
       lines.append(' '.join(current_line))


   # Desenhando o título centralizado linha por linha
   for i, line in enumerate(lines):
       draw_centered_text(c, line, y_position - i*(font_size + 5), width, font_name, font_size)




def draw_centered_text(c, text, y_position, width, font_name, font_size):
   text_width = c.stringWidth(text, font_name, font_size)
   x_position = (width - text_width) / 2 
  
   c.drawString(x_position, y_position, text)

def draw_centered_text_with_offset(c, text, y_position, width, font_name, font_size, x_offset=0, max_width=None, max_lines=None):
    # Verifica se max_width e max_lines foram fornecidos
    if max_width is None:
        max_width = width  # Use a largura máxima da página por padrão
    if max_lines is None:
        max_lines = 4  # Use um máximo de 4 linhas por padrão

    words = text.split(' ')
    lines = []
    current_line = []

    # Constrói as linhas baseado na largura máxima e no número máximo de linhas
    for word in words:
        if len(lines) >= max_lines:
            break  # Alcançou o número máximo de linhas permitido
        if c.stringWidth(' '.join(current_line + [word]), font_name, font_size) <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))

    text_height = len(lines) * (font_size + 5)  # Altura total do texto
    y_position -= text_height / 2  # Ajusta a posição vertical para o centro

    x_position = (width - max_width) / 2 + x_offset  # Aplica o deslocamento horizontal

    for i, line in enumerate(lines):
        draw_centered_text(c, line, y_position - i * (font_size + 5), width, font_name, font_size)

    return y_position - len(lines) * (font_size + 5)  # Retorna a nova posição vertical após desenhar o texto

def add_name_and_coauthor_to_certificate(pdf_path, output_path, name, title, coauthor):
    print(f"Processando o nome: {name}")

    custom_size = (29.70 * cm, 21.00 * cm)  # Define o tamanho customizado

    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=custom_size)  # Usa o tamanho customizado
        width, height = custom_size  # Usa o tamanho customizado

        # Colocando o título.
        font_size_title = 16
        c.setFont("Poppins-Bold", font_size_title)
        max_title_width = 23 * cm
        c.setFillColorRGB(0.07, 0.08, 0.3)  # Azul escuro
        draw_title_text(c, title, height/2 + 18, width, "Poppins-Bold", font_size_title, max_title_width)

        # Adicione o nome do coautor abaixo do título
        font_size_coauthor = 12
        max_width_coauthor = 15 * cm  # Largura máxima para o texto dos coautores
        max_lines_coauthor = 4  # Número máximo de linhas para o texto dos coautores
        x_offset_coauthor = -7 * cm  # Ajuste o valor conforme necessário

        y_position = height / 2 - 30 - font_size_title  # Posição inicial

        # Use a função draw_title_text para desenhar os coautores
        y_position = draw_title_text(c, coauthor, y_position, width, "Poppins", font_size_coauthor, max_width_coauthor)

        font_size = 22
        c.setFont("Poppins", font_size)
        c.setFillColorRGB(0.2, 0.2, 0.5)  # Azul médio acinzentado

        if c.stringWidth(name, "Poppins", font_size) > width - 50:
            parts = name.split(' ')
            halfway = len(parts) // 2
            name_line_1 = ' '.join(parts[:halfway])
            name_line_2 = ' '.join(parts[halfway:])

            draw_centered_text(c, name_line_1, height/2 + font_size/3 - 30, width, "Poppins", font_size)
            draw_centered_text(c, name_line_2, height/2 - font_size/2 - 38, width, "Poppins", font_size)
        else:
            draw_centered_text(c, name, height/2 + 60, width, "Poppins", font_size)

        c.save()

        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        page = pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

    print(f"Certificado para {name} concluído!")


def main():
   with open(ap_orais_path, 'r', encoding='utf-8-sig') as f_names, \
           open('/home/leticia/Downloads/Emissor de certificado automático/titulos_ap_orais.txt', 'r', encoding='utf-8-sig') as f_titles, \
           open('/home/leticia/Downloads/Emissor de certificado automático/coautores_ap_orais.txt', 'r', encoding='utf-8-sig') as f_coauthors:


       names = f_names.readlines()
       titles = f_titles.readlines()
       coauthors = f_coauthors.readlines()


       for name, title, coauthor in zip(names, titles, coauthors):
           cleaned_name = name.strip()
           cleaned_title = title.strip()
           cleaned_coauthor = coauthor.strip()


           output_path = f"/home/leticia/Downloads/Emissor de certificado automático/certificados_apresentadores_orais/certificado_apresentador(a)_oral_{cleaned_name}.pdf"


           add_name_and_coauthor_to_certificate(modelo_ap_oral_path, output_path, cleaned_name, cleaned_title, cleaned_coauthor)
           print(f"Certificado gerado para {cleaned_name} em {output_path}")




if __name__ == '__main__':
   main()




