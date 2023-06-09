# Copyright 2023 SAP SE
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from osc_lib.command import command

from osc_placement.resources.trait import FIELDS, RP_BASE_URL, RP_TRAITS_URL
from osc_placement import version


class BaseTraitCommand(command.Lister):

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'uuid',
            metavar='<uuid>',
            help='UUID of the resource provider.'
        )

        parser.add_argument(
            'traits',
            metavar='<trait>',
            nargs='+',
            help='Name of the trait(s).',
        )

        return parser

    @version.check(version.ge('1.6'))
    def take_action(self, parsed_args):
        http = self.app.client_manager.placement

        url = RP_BASE_URL.format(uuid=parsed_args.uuid)
        rp = http.request('GET', url).json()
        url = RP_TRAITS_URL.format(uuid=parsed_args.uuid)

        # we fetch the traits to have the full list to add/remove the given one
        rp_traits = set(http.request('GET', url).json()['traits'])
        if self.operation == 'remove':
            traits_to_remove = set(parsed_args.traits)
            non_existing_traits = traits_to_remove - rp_traits
            for trait in non_existing_traits:
                print(f"Info: Trait {trait} was already not set on {parsed_args.uuid}")
            if non_existing_traits == traits_to_remove:
                print(f"Info: No action taken as non of the given traits was set")
                return FIELDS, [[t] for t in rp_traits]
            rp_traits -= traits_to_remove
        elif self.operation == 'add':
            traits_to_add = set(parsed_args.traits)
            existing_traits = rp_traits & traits_to_add
            for trait in existing_traits:
                print(f"Info: Trait {trait} is already set on {parsed_args.uuid}")
            if existing_traits == traits_to_add:
                print(f"Info: No action taken as all of the given traits were set already")
                return FIELDS, [[t] for t in rp_traits]
            rp_traits |= traits_to_add
        else:
            raise ValueError(f"Unexpected value for operation: {self.operation}")

        payload = {
            'resource_provider_generation': rp['generation'],
            'traits': list(rp_traits)
        }
        traits = http.request('PUT', url, json=payload).json()['traits']
        return FIELDS, [[t] for t in traits]


class AddTrait(BaseTraitCommand):
    operation = 'add'


class RemoveTrait(BaseTraitCommand):
    operation = 'remove'
