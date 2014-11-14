# -*- coding: utf-8 -*-
"""
matinbonheur.core

Created by schminitz
"""

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

import email


class CommandView(BrowserView):
    """
    """

    email_content = (
        u"Bonjour,\r\n\r\n"
        u"Cet e-mail vous est envoyé automatiquement pour vous informer "
        u"qu'une commande a été effectuée par "
        u": %(firstname)s %(lastname)s (téléphone: %(phone)s).\r\n\r\n"
        u"Voici sa commande:\r\n\r\n"
        u"Paniers 1: %(panier_1)s\r\n"
        u"Paniers 2: %(panier_2)s\r\n"
        u"Paniers 3: %(panier_3)s\r\n"
        u"Croissants: %(croissant)s\r\n"
        u"Pains au chocolat: %(pain_chocolat)s\r\n\r\n"
        u"Il aimerait être livré vers %(hour)s:%(minute)s\r\n\r\n"
        u"Et voici son message personnalisé:\r\n"
        u"%(message)s\r\n\r\n"
        u"Bien cordialement,\r\n\r\nLe site Matin bonheur")

    @property
    def values(self):
        values = {}
        # Get datas
        rg = self.request.get

        values['lastname'] = rg('lastname', '').decode('utf-8')
        values['firstname'] = rg('firstname', '').decode('utf-8')
        values['phone'] = rg('phone', '').decode('utf-8')
        values['hour'] = rg('hour', '')
        values['minute'] = rg('minute', '')
        values['panier_1'] = rg('panier_1', '')
        values['panier_2'] = rg('panier_2', '')
        values['panier_3'] = rg('panier_3', '')
        values['croissant'] = rg('croissant', '')
        values['pain_chocolat'] = rg('pain_chocolat', '')
        values['message'] = rg('message', '').decode('utf-8')
        return values

    def treat_command(self):
        """
        Validate and send command
        """
        if not self.request.get('form_sent') == "1":
            return {'not_sent': True, 'message': ""}

        # Validate
        status = self.validate()
        if status != "":
            return {'not_sent': True, 'message': status}

        # Send email
        self.send_email()

        return {'not_sent': False, 'message': u"Votre commande a bien été envoyée!"}

    @property
    def email_message(self):
        """ Returns the email message """
        values = self.values
        content = self.email_content % values
        message = email.message_from_string(content.encode('utf-8'))
        message.set_charset('utf-8')
        message['X-Priority'] = email.Header.Header('1')
        return message

    def send_email(self):
        """ Sends the email """
        self.mailhost.secureSend(
            self.email_message,
            u'gaetanmiot@hotmail.com',
            u'Matin bonheur <info@matinbonheur.be>',
            subject=(u"Commande de paniers Matin bonheur"),
            charset='utf-8')

    def validate(self):
        """
        Nom, Prénom, N° de téléphone doivent être remplis

        Au moins une formule doit être au dessus de 0
        """
        status = ""
        values = self.values

        if not values['lastname']:
            status += u"Veuillez indiquer votre nom.<br />"
        if not values['firstname']:
            status += u"Veuillez indiquer votre prénom.<br />"
        if not values['phone']:
            status += u"Veuillez indiquer votre numéro de téléphone.<br />"

        if values['panier_1'] == "0" and values['panier_2'] == "0" and values['panier_3'] == "0":
            status += u"Veuillez commander au moins une des formules.<br />"

        return status

    @property
    def mailhost(self):
        """ Returns the mail host from Plone """
        return getToolByName(self.context, 'MailHost')
