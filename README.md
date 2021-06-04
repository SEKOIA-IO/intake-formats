# Intakes

Welcome to the SEKOIA.IO Intakes repository! This repository contains all our latest intakes definitions: parsers.

# Contributing to the docs

You can click the Fork button in the upper-right area of the screen to create a copy of this repository in your GitHub account. This copy is called a fork. Make any changes you want in your fork, and when you are ready to send those changes to us, go to your fork and create a new pull request to let us know about it.

Once your pull request is created, a SEKOIA.IO reviewer will take responsibility for providing clear, actionable feedback.


# What is an intake

SEKOIA.IO generates events from several sources (transport and formats). It is a data source for the client. This could be a system like Linux or Windows or a firewall like Fortigate or Netfilter.

Each source has a precise format, that is why we distinguish all of them. This lets us know the severity of an alert: suspicious traffic blocked by a Linux machine but not firstly by the firewall so we have to inform the customer of modifying his firewall configuration. To collect the client data, we created parsers.

For questions and feedback, please contact support@sekoia.io
