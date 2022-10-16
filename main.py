from db_config import local_session, create_all_entities
from db_repo import DbRepo
from facade.FacadeBase import FacadeBase
repo = DbRepo(local_session)

# repo.delete_all_tables()
create_all_entities()
# repo.reset_db()


