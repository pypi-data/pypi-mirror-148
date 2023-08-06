# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Entropy Markets](https://entropy.trade/) support is available at:
#   [Docs](https://docs.entropy.trade/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/entropymarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import argparse
import entropy
import typing

from decimal import Decimal

from .element import Element
from ...modelstate import ModelState


# # 🥭 RoundToLotSizeElement class
#
# May modifiy an `Order`s price or quantity to ensure it's exactly aligned to the market's lot sizes.
#
class RoundToLotSizeElement(Element):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def add_command_line_parameters(parser: argparse.ArgumentParser) -> None:
        pass

    @staticmethod
    def from_command_line_parameters(
        args: argparse.Namespace,
    ) -> "RoundToLotSizeElement":
        return RoundToLotSizeElement()

    def process(
        self,
        context: entropy.Context,
        model_state: ModelState,
        orders: typing.Sequence[entropy.Order],
    ) -> typing.Sequence[entropy.Order]:
        new_orders: typing.List[entropy.Order] = []
        for order in orders:
            new_price: Decimal = model_state.market.lot_size_converter.round_quote(
                order.price
            )
            new_quantity: Decimal = model_state.market.lot_size_converter.round_base(
                order.quantity
            )
            new_order: entropy.Order = order.with_update(price=new_price).with_update(
                quantity=new_quantity
            )
            if new_order.price == 0 or new_order.quantity == 0:
                self._logger.debug(
                    f"""Order removed - price or quantity rounded to zero:
    Old: {order}
    New: {new_order}"""
                )
            elif (order.price != new_order.price) or (
                order.quantity != new_order.quantity
            ):
                new_orders += [new_order]
                self._logger.debug(
                    f"""Order change - price and quantity now aligned to lot size:
    Old: {order}
    New: {new_order}"""
                )
            else:
                new_orders += [order]

        return new_orders

    def __str__(self) -> str:
        return "« RoundToLotSizeElement »"
