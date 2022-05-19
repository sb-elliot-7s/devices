import random

from randmac import RandMac
from sqlalchemy import insert, select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models import Device, Endpoint


class Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _save_endpoints(self, device_id):
        query = insert(Endpoint).values([{'endpoint': 'https://google.com', 'device_id': device_id[i]} for i in range(5)])
        _ = await self._session.execute(query)
        await self._session.commit()

    async def save_devices(self):
        dev_type = ('emeter', 'zigbee', 'lora', 'gsm')
        result = await self._session.execute(insert(Device).values([
            {'dev_id': str(RandMac()), 'dev_type': random.choice(dev_type)} for _ in range(10)]).returning(Device.dev_id))
        await self._session.commit()
        returned_ids = result.scalars().all()[:5]
        await self._save_endpoints(device_id=returned_ids)

    async def get_devices(self):
        """
            select d.dev_type, count(d.dev_type) num_device_type
            from devices d
            left join endpoints e on e.device_id = d.dev_id
            where e.device_id is NULL
            group by d.dev_type
            order by num_device_type desc
        """
        query = select(Device.dev_type, func.count(Device.dev_type).label('number_of_device_types')) \
            .outerjoin(Endpoint) \
            .where(Endpoint.device_id.is_(None)) \
            .group_by(Device.dev_type) \
            .order_by(desc('number_of_device_types'))
        result = await self._session.execute(query)
        return result.all()
