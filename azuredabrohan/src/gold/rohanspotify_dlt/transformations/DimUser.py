import dlt

expectations = {
    "rule1" : "user_id IS NOT NULL",
    "rule2" : "user_name IS NOT NULL"
}

@dlt.table
def dimuser_stg():
    df=spark.readStream.table("spotify_cata.silver.dimuser")
    return df

dlt.create_streaming_table(name= "dimuser", expect_all_or_drop=expectations)
dlt.create_auto_cdc_flow(
    target="dimuser",
    source="dimuser_stg",
    keys=["user_id"],
    sequence_by="updated_at",
    stored_as_scd_type=2,
    name=None,
    once=False
)