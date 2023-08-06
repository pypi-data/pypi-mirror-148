from positionrepo.Position import Position
from positionrepo.repository.PositionRepository import PositionRepository

from position.provider.supplier.PositionSupplier import PositionSupplier


class PositionProvider:

    def __init__(self, position_supplier: PositionSupplier, position_repository: PositionRepository):
        self.position_supplier = position_supplier
        self.position_repository = position_repository

    def obtain_position(self) -> Position:
        # todo: based on position slip (controlled here)
        position = self.position_supplier.fetch_position()
        self.position_repository.store(position)
        return position
