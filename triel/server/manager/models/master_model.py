"""

 Copyright 2020 Teros Technology

 Ismael Perez Rojo
 Carlos Alberto Ruiz Naranjo
 Alfredo Saez

 This file is part of Triel.

 Triel is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Triel is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Colibri.  If not, see <https://www.gnu.org/licenses/>.

"""

from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Simulator(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    path = models.CharField(max_length=512, null=True)
    languages = models.ManyToManyField(Language, related_name="simulators", blank=False, editable=False)


class Suite(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    simulators = models.ManyToManyField(Simulator, related_name="suites", blank=False, editable=False)


