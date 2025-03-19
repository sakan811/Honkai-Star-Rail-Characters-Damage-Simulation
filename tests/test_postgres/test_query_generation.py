from hsr_simulation.postgre import generate_dmg_view_query


def test_generate_dmg_view_query():
    """Test damage view query generation"""
    view_name = "test_view"
    stage_table = "test_stage"

    query = generate_dmg_view_query(view_name, stage_table)

    # Verify query contains key components
    assert f'CREATE OR REPLACE VIEW public."{view_name}"' in query
    assert f'FROM public."{stage_table}"' in query
    assert 'GROUP BY "Character"' in query
    assert 'ORDER BY "Character"' in query
