from couchdb_compose.composer import actions

def test_streamsapp(composer):
    composer.run_actions(actions)
