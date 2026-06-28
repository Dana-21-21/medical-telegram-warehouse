with source as (

    select * from raw.telegram_messages

),

cleaned as (

    select
        message_id,
        channel_name,
        channel_username,

        message_date::timestamp as message_date,

        message_text,

        case
            when message_text is null or trim(message_text) = '' then false
            else true
        end as has_text,

        has_media,

        case
            when has_media then true
            else false
        end as has_image,

        image_path,

        coalesce(views,0) as views,

        coalesce(forwards,0) as forwards,

        length(coalesce(message_text,'')) as message_length

    from source

)

select *
from cleaned
