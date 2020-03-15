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

from rest_framework import serializers

from triel.server.manager.models.master_model import Language, Simulator, Suite
from triel.simulator.validator import validate_simulator


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class SimulatorSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    def validate_path(self, path):
        return validate_simulator(self.instance.name, path)

    class Meta:
        model = Simulator
        fields = '__all__'


class SimulatorNestedSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Simulator
        fields = ('id', 'name', 'languages')


class SuiteSerializer(serializers.ModelSerializer):
    simulators = SimulatorNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Suite
        fields = '__all__'
