import dlt

expectations = {
    "rule1" : "track_id IS NOT NULL",
    "rule2" : "track_name IS NOT NULL"
}
    

@dlt.table
@dlt.expect_all_or_drop(expectations)
def dimtrack_stg():
    df=spark.readStream.table("spotify_cata.silver.dimtrack")
    return df

dlt.create_streaming_table("dimtrack")
dlt.create_auto_cdc_flow(
    target="dimtrack",
    source="dimtrack_stg",
    keys=["track_id"],
    sequence_by="updated_at",
    stored_as_scd_type=2,
    name=None,
    once=False
)