from bs4 import BeautifulSoup
import imaplib
import email
import json
import socket
import sys

def convert_stanje_to_float(stanje):
    stanje = stanje.replace(' ', '')
    stanje = stanje.replace('.', '')
    stanje = stanje.replace(',', '.')
    return float(stanje)

def get_from_imap():
    try:
        #email_user = input('Email: ')
        #email_pass = input('Lozinka: ')
        #imap_host = input('IMAP host: ')
        #imap_port = input('IMAP port: ')
        email_user = 'gluvajic@aol.com'
        email_pass = 'okjxdpzfzdzqbmlp'
        imap_host = 'export.imap.aol.com'
        imap_port = 993

        server = imaplib.IMAP4_SSL(imap_host, imap_port)
        server.login(email_user, email_pass)

        server.select('inbox')

        result, data = server.search(None, '(FROM "faxserver@erstebank.rs")')
        for num in data[0].split():
            mail_result, mail_data = server.fetch(num, '(RFC822)')
            raw_email = mail_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            extract_izvod(raw_email_string);

    except Exception as e:
        print(str(e))

def extract_izvod(raw_email_string):
    try:
        email_message = email.message_from_string(raw_email_string)

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()

            if bool(filename) and filename.endswith('.htm'):
                parse_file(part.get_payload(decode=True), filename)
    except Exception as e:
        print(str(e))

def parse_file(payload, filename):
    try:
        soup = BeautifulSoup(payload, 'html.parser')

        data_dict = {};
        data_dict['broj_racuna'] = soup.body.find('table').find_all('td')[1].string
        data_dict['datum'] = soup.body.find('table').find_all('td')[5].string
        data_dict['novo_stanje'] = convert_stanje_to_float(soup.body.find_all('b')[12].string)

        file = open('data.json', 'w')
        file.write(json.dumps(data_dict))
        file.close()

        print('Svi podaci su ispisani u fajl data.json!')

    except Exception as e:
        print(str(e))

def get_from_socket():

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_address = sys.argv[1]
    sock.bind(server_address)

    sock.listen(5)
    while True:
        c, addr = sock.accept()
        data = c.recv(1024)
        print(data.decode('utf-8'))

        c.send(extract_izvod(data))

    c.close()

get_from_socket()
