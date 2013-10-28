# Copyright (c) 2013, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.


from nose.plugins.attrib import attr as noseattr
from qa_tests import risk


class EventBaseQATestCase(risk.CompleteTestCase, risk.FixtureBasedQATestCase):
    hazard_calculation_fixture = ("QA (regression) test for Risk Event "
                                  "Based from Stochastic Event Set")

    @noseattr('qa', 'risk', 'event_based')
    def test(self):

        expected_losses = [
            92.2926045589, 24.0955037795, 15.2574877424, 4.13173076809,
            3.62888022928, 2.39812650903, 1.88800594048, 1.58418916667,
            1.43912920116, 0.788863729912, 0.693836556766, 0.59031512009,
            0.394335695369, 0.215708199815, 0.21144108574, 0.199652819341,
            0.188879150589, 0.117552020148, 0.109518261565, 0.0606121379835,
            0.0520004106134, 0.0401384025087, 0.0305615344323, 0.013685031793]

        outputs = self._run_test().output_set
        losses = outputs.get(output_type="event_loss").event_loss

        for event_loss, expected in zip(losses, expected_losses):
            self.assertAlmostEqual(
                expected, event_loss.aggregate_loss,
                msg="loss for rupture %r is %s (expected %s)" % (
                    event_loss.rupture.tag, event_loss.aggregate_loss,
                    expected))

        disagg_gen = outputs.get(
            output_type="loss_fraction",
            loss_fraction__variable="coordinate").loss_fraction.iteritems()

        print outputs.get(
            output_type="loss_fraction",
            loss_fraction__variable="coordinate").loss_fraction.id
        disagg = list(disagg_gen)

        self.assertEqual(1, len(disagg))

        [(coords, values)] = disagg

        self.assertEqual((83.313823, 29.236172), coords)

        expected = {
            '80.0000,82.0000|28.0000,30.0000': (0.1350454689871,
                                                0.0016942753673914457),
            '82.0000,84.0000|26.0000,28.0000': (0.334522875484,
                                                0.004196911395936113),
            '82.0000,84.0000|28.0000,30.0000': (7.93354729428041,
                                                0.0995339855350374),
            '82.0000,84.0000|30.0000,32.0000': (63.962514900726,
                                                0.8024713027806971),
            '84.0000,86.0000|26.0000,28.0000': (0.538213632029,
                                                0.00675240795548738),
            '84.0000,86.0000|28.0000,30.0000': (3.296389565305,
                                                0.041356379326995076),
            '84.0000,86.0000|30.0000,32.0000': (3.5066849767739,
                                                0.04399473763845564)}
        self.assertEqual(expected, dict(values))
