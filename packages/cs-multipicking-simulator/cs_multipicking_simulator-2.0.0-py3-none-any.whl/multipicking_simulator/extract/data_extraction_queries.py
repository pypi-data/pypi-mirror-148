"""
This file is meant to store all SQL and DataDog queries related to data extraction.

4 Superpal queries are currently stored in this file:
    - actual_mpd_pairs_query (Actual delivered MP order pairs extraction)
    - daily_zone_mpd_stats_query (Daily % MPD statistics extraction)
    - mpd_precandidates_query (OM admitted orders)
    - order_detail_query (Extracts important detail of the order's characteristics)
    - opzone_mp_settings_parameter_query (Op Zone MP Settings extraction)
"""

def zone_tuple_str(zone_ids_tuple: tuple) -> str:
    if len(zone_ids_tuple) == 1:
        return f'({zone_ids_tuple[0]})'
    else:
        return zone_ids_tuple


def actual_mpd_pairs_query(dates_tuple: tuple, zone_ids_tuple:tuple) -> str:
    """
    Returns the SQL query to retrieve the actual delivered MP order pairs for the given dates and zones.

    Parameters
    ----------
    dates_tuple (tuple):
        tuple containing each required date as a 'yyyy-mm-dd' formatted string.
    zone_ids_tuple (tuple):
        tuple containing each required zone's ID as an integer.

    Returns
    -------
    query (str):
        SQL query.
    """
    query = f"""
        SELECT
            DISTINCT o1.id AS order_id_1,
            om1.value::integer AS order_id_2,
            o1.shopper_picking_id,
            o2.shopper_picking_id,
            om1.key,
            om2.key,
            om3.key,
            om4.key,
            om5.key,
            geo_opzone.id as customer_zone_id,
            (o1.actual_delivery_time at time zone gc.timezone)::date as date
        FROM
            orders_order o1
            JOIN orders_ordermetadata om1 ON o1.id=om1.order_id AND om1.key IN ('is_multipicking_parent_for_order', 'is_multipicking_child_for_order') --primero el par
            JOIN orders_order o2 ON o2.id=om1.value::integer AND o2.order_kind = 'NORMAL' AND o2.shopper_picking_id=o1.shopper_picking_id
            JOIN orders_ordermetadata om2 ON o1.id=om2.order_id AND om2.key='multipicking_dispatcher' --el papa dispatcher
            JOIN orders_ordermetadata om3 ON o2.id=om3.order_id AND om3.key='multipicking_dispatcher' -- el hijo dispatcher
            LEFT JOIN orders_ordermetadata om4 ON o1.id=om4.order_id AND om4.key = 'multipicking_not_required_picking' -- el papa no mpnrp
            LEFT JOIN orders_ordermetadata om5 ON o2.id=om5.order_id AND om5.key = 'multipicking_not_required_picking' -- el papa no mpnrp
            JOIN geo_opzone ON o1.customer_zone_id=geo_opzone.id
            JOIN geo_city gc ON gc.id = o1.customer_city_id
        WHERE
            geo_opzone.id in {zone_tuple_str(zone_ids_tuple)}
            AND o1.actual_delivery_time > '{min(dates_tuple)}'::date - interval '2 days'
            AND (o1.actual_delivery_time at time zone gc.timezone)::date in {dates_tuple}
            AND om4.key IS NULL AND om5.key IS NULL
            AND o1.status = 'DELIVERED'
            AND o1.order_kind = 'NORMAL'
    """
    return query


def daily_zone_mpd_stats_query(dates_tuple: tuple, zone_ids_tuple:tuple) -> str:
    """
    Returns the SQL query to retrieve the MPD% statistics for the given dates and zones.
    This includes %MPD over total orders and %MPD over total scheduled orders.

    Parameters
    ----------
    dates_tuple (tuple):
        tuple containing each required date as a 'yyyy-mm-dd' formatted string.
    zone_ids_tuple (tuple):
        tuple containing each required zone's ID as an integer.

    Returns
    -------
    query (str):
        SQL query.
    """

    query = f"""
        WITH datos AS (
            SELECT
                to_char(o.actual_delivery_time at time zone geo_city.timezone , 'yyyy-mm-dd') as fecha,
                o.id as order_id,
                o.customer_zone_id as customer_zone_id,
                o.on_demand,
                case when om.key is null then 'Single' else 'Multipicking' end order_type,
                case when (om.key is not null and om2.key = 'multipicking_dispatcher') then 'multipicking_dispatcher'
                    when (om.key is not null and om2.key is null) then 'multipicking_bot'
                    else null
                    END AS multipicking_type,
                case when o.actual_delivery_time > o.promised_delivery_time then 'late'
                    when o.actual_delivery_time < o.min_delivery_time then 'early'
                    else 'on time'
                    END AS status_time,
                om2.key key2,
                om3.key key3,
                om4.key key4,
                om5.key key5
            FROM
                orders_order o
                JOIN geo_city on geo_city.id = o.customer_city_id
                JOIN geo_opzone ON o.customer_zone_id=geo_opzone.id and not geo_opzone.deleted
                LEFT JOIN orders_ordermetadata om on o.id=om.order_id and om.key IN ('is_multipicking_parent_for_order','is_multipicking_child_for_order')
                LEFT JOIN orders_order o2 on o2.id=om.value::integer and  o2.status = 'DELIVERED' and o2.order_kind = 'NORMAL' and  o2.shopper_picking_id=o.shopper_picking_id
                LEFT JOIN orders_ordermetadata om2 on o.id=om2.order_id and om2.key = 'multipicking_dispatcher'
                LEFT JOIN orders_ordermetadata om3 ON o2.id=om3.order_id AND om3.key='multipicking_dispatcher' -- el hijo dispatcher
                LEFT JOIN orders_ordermetadata om4 ON o.id=om4.order_id AND om4.key = 'multipicking_not_required_picking' -- el papa no mpnrp
                LEFT JOIN orders_ordermetadata om5 ON o2.id=om5.order_id AND om5.key = 'multipicking_not_required_picking' -- el papa no mpnrp
            WHERE
                o.actual_delivery_time > '{min(dates_tuple)}'::date - interval '2 days'
                AND (o.actual_delivery_time at time zone geo_city.timezone)::date in {dates_tuple}
                AND o.order_kind <> 'GIFT_ORDER'
                AND o.status = 'DELIVERED'
                AND o.customer_zone_id in {zone_tuple_str(zone_ids_tuple)}
            ORDER BY
                1 DESC, 3  DESC
        )

        SELECT
            d.customer_zone_id, d.fecha as date,
            count (distinct d.order_id) as total_day_orders,
            count (distinct d.order_id)filter(where d.on_demand = False) as total_scheduled_orders,
            count (distinct d.order_id)filter (WHERE d.multipicking_type = 'multipicking_dispatcher' and key2 IS not NULL AND key3 is not null and key4 IS NULL AND key5 IS NULL) as total_orders_mp,
            count (distinct d.order_id)filter (WHERE d.multipicking_type = 'multipicking_dispatcher' and key2 IS not NULL AND key3 is not null and key4 IS NULL AND key5 IS null and d.on_demand = False) as total_scheduled_orders_mp,
            case when count (distinct d.order_id) = 0 THEN 0 ELSE (count (distinct d.order_id) filter (WHERE d.multipicking_type = 'multipicking_dispatcher' and key2 IS not NULL AND key3 is not null and key4 IS NULL AND key5 IS NULL)/ (count (distinct d.order_id) )::float)*100 END as dispatcher_pct,
            case when count (distinct d.order_id)filter (where d.on_demand = False) = 0 THEN 0 ELSE (count (distinct d.order_id) filter (WHERE d.multipicking_type = 'multipicking_dispatcher' and key2 IS not NULL AND key3 is not null and key4 IS NULL AND key5 IS NULL)/ (count (distinct d.order_id)filter (where d.on_demand = False) )::float)*100 END as pct_multipicking_oos
        FROM
            datos d
        GROUP BY
            1, 2
     """

    return query


def mpd_precandidates_query(dates_tuple: tuple, zone_ids_tuple: tuple) -> str:
    """
    Returns the SQL query to retrieve all MPD precandidate orders for the given dates and zones.

    Parameters
    ----------
    dates_tuple (tuple):
        tuple containing each required date as a 'yyyy-mm-dd' formatted string.
    zone_ids_tuple (tuple):
        tuple containing each required zone's ID as an integer.

    Returns
    -------
    query (str):
        SQL query.
    """

    query = f"""
        SELECT
            DISTINCT o.id,
            o.customer_zone_id AS customer_zone_id,
            (o.actual_delivery_time AT TIME ZONE geo_city.timezone)::DATE AS date
        FROM orders_order AS o
            JOIN geo_city ON geo_city.id = o.customer_city_id
            LEFT JOIN orders_ordermetadata AS om ON om.order_id = o.id AND om.key = 'ON_DEMAND_ASAP'
        WHERE
            o.actual_delivery_time >= '{min(dates_tuple)}'::DATE - INTERVAL '2 days'
            AND (o.actual_delivery_time AT TIME ZONE geo_city.timezone)::DATE IN {dates_tuple}
            AND o.customer_zone_id IN {zone_tuple_str(zone_ids_tuple)}
            AND o.status = 'DELIVERED'
            AND NOT (o.on_demand IS TRUE AND om.key IS NULL)
            AND o.order_kind NOT IN ('POST_SALE','GIFT_ORDER')
        ORDER BY 1
    """
    return query


def order_detail_query(ids_tuple_str: str) -> str:
    """
    Returns the SQL query to retrieve the detail for the given Order IDs.

    Parameters
    ----------
    ids_tuple_str (str):
        String-formatted tuple containing the required Order IDs.

    Returns
    -------
    query (str):
        SQL query.
    """

    query = f"""
        WITH custom_products AS (
            SELECT
                o.id order_id,
                count(ocp.id) AS custom_products
            FROM
                orders_order o
                LEFT JOIN orders_ordercustomproduct AS ocp ON ocp.order_id = o.id AND ocp.created_by = 'CUSTOMER'
            WHERE
                o.id IN {ids_tuple_str}
                AND o.order_kind = 'NORMAL'
            GROUP BY 1
        )
        SELECT
            o.id AS order_id,
            count(distinct op.product_id) AS products_ordered,
            o.order_kind,
            gc.country_id AS country,
            o.customer_city_id AS city_id,
            gc.name AS city_name,
            gc.timezone,
            o.customer_zone_id as customer_zone_id,
            (o.actual_delivery_time at time zone gc.timezone)::date as date,
            cs.name AS store_name,
            cs.id AS store_id,
            o.store_branch_id,
            gop.id AS branch_zone_id,
            st_astext(o.customer_location) AS customer_location,
            st_astext(csb.picking_point) AS branch_location,
            (o.created at time zone gc.timezone) AS created,
            (o.picking_assignable_time at time zone gc.timezone) AS picking_assignable_time,
            (o.min_delivery_time at time zone gc.timezone) AS min_delivery_time,
            (o.promised_delivery_time at time zone gc.timezone) AS promised_datetime,
            o.on_demand,
            CASE WHEN omm.key is NULL THEN False ELSE True END AS is_asap,
            ro.parent_id,
            COUNT(DISTINCT CASE
                WHEN op.buy_unit = 'UN' THEN op.product_id
                ELSE NULL
                END) AS n_products_by_unit,
            COUNT(DISTINCT CASE
                WHEN op.buy_unit != 'UN' THEN op.product_id
                ELSE NULL
                END) AS n_products_by_weight,
            SUM(CASE
                WHEN op.buy_unit = 'UN' THEN cp.weight * op.quantity
                ELSE op.quantity
                END) AS total_weight,
            COUNT(DISTINCT ca.category_id) AS unique_categories,
            COUNT(DISTINCT cpl.id) AS unique_top_level_categories,
            SUM(DISTINCT ocp.custom_products) AS n_custom_products,
            CASE
                WHEN COUNT(c.product_id) > 0 THEN TRUE
                ELSE FALSE
                END has_frozen_product
        FROM
            orders_order o
            JOIN catalog_storebranch AS csb ON csb.id = o.store_branch_id
            JOIN geo_opzone AS gop ON st_intersects(csb.location, gop.multi_poly)
            JOIN geo_city AS gc ON gc.id = gop.city_id
            JOIN catalog_store AS cs ON cs.id = csb.store_id
            JOIN orders_orderproduct AS op ON op.order_id = o.id AND op.created_by = 'CUSTOMER'
            LEFT JOIN catalog_product AS cp ON cp.id = op.product_id
            LEFT JOIN catalog_productcategorization AS ca ON ca.product_id = cp.id
            LEFT JOIN catalog_category AS cat ON cat.id = ca.category_id
            LEFT JOIN catalog_category AS cpl ON cpl.tree_id = cat.tree_id AND cpl.level = 0
            LEFT JOIN orders_relatedorder AS ro ON o.id=ro.parent_id AND ro.relation_type='GIFT_ORDER'
            LEFT JOIN catalog_producttag AS c ON c.product_id = op.product_id AND c.tag_id = 8
            LEFT JOIN custom_products AS ocp ON ocp.order_id = o.id
            LEFT JOIN orders_ordermetadata AS omm ON omm.order_id = o.id AND omm.key = 'ON_DEMAND_ASAP'
        WHERE
            o.id IN {ids_tuple_str}
            AND gop.deleted = FALSE
            AND o.order_kind = 'NORMAL'
        GROUP BY
            1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22
        ORDER BY
            1
    """

    return query


def opzone_mp_settings_parameter_query() -> str:
    """
    Returns the SQL query to retrieve the MP_SETTINGS parameter values for all Op Zones.

    Returns
    -------
    query (str):
        SQL query.
    """

    query = """
        SELECT
            *
        FROM
            geo_opzoneparameter as gop
            JOIN geo_opzone as go on go.id = gop.zone_id
            JOIN geo_city as gc on go.city_id = gc.id
        WHERE
            gop.parameter = 'MULTIPICKING_SETTINGS'
        """

    return query


def athena_order_detail_query(ids_tuple_str: str) -> str:

    query = f"""
        WITH custom_products AS (
            SELECT
                ocp.order_id,
                COUNT(ocp.id) AS custom_products
            FROM
                orders_ordercustomproduct ocp
            WHERE
                ocp.created_by = 'CUSTOMER'
                AND order_id IN {ids_tuple_str}
            GROUP BY
                ocp.order_id
        )

        SELECT
            o.id AS order_id,
            o.qty_products_ordered AS products_ordered,
            o.order_kind,
            gc.country_id AS country,
            o.customer_city_id AS city_id,
            gc.name AS city_name,
            gc.timezone,
            o.customer_zone_id,
            DATE(AT_TIMEZONE(o.actual_delivery_time, gc.timezone)) AS date,
            cs.name AS store_name,
            cs.id AS store_id,
            o.store_branch_id,
            ST_AsText(ST_Point(oa.lng, oa.lat)) AS customer_location,
            ST_AsText(ST_Point(csb.lng, csb.lat)) AS branch_location,
            AT_TIMEZONE(o.picking_assignable_time, gc.timezone) AS picking_assignable_time,
            AT_TIMEZONE(o.min_delivery_time, gc.timezone) AS min_delivery_time,
            AT_TIMEZONE(o.promised_delivery_time, gc.timezone) AS promised_datetime,
            COUNT(DISTINCT CASE
                WHEN op.buy_unit = 'UN' THEN op.product_id
                ELSE NULL END) AS n_products_by_unit,
            COUNT(DISTINCT CASE
                WHEN op.buy_unit != 'UN' THEN op.product_id
                ELSE NULL END) AS n_products_by_weight,
            SUM(CASE
                WHEN op.buy_unit = 'UN' THEN cp.weight * op.quantity
                ELSE op.quantity END) AS total_weight,
            COUNT(DISTINCT cc.id) AS unique_categories,
            COUNT(DISTINCT cc_tl.id) AS unique_top_level_categories,
            SUM(DISTINCT cst_p.custom_products) AS n_custom_products,
            CASE
                WHEN COUNT(cpt.product_id) > 0 THEN TRUE
                ELSE FALSE END AS has_frozen_product
        FROM
            orders_order o
            JOIN orders_orderaddress oa ON oa.order_id = o.id
            JOIN geo_opzone go ON o.customer_zone_id = go.id
            JOIN geo_city gc ON go.city_id = gc.id
            JOIN catalog_storebranch csb ON o.store_branch_id = csb.id
            JOIN catalog_store cs ON csb.store_id = cs.id
            LEFT JOIN orders_orderproduct op ON op.order_id = o.id AND op.created_by = 'CUSTOMER'
            LEFT JOIN catalog_product cp ON op.product_id = cp.id
            LEFT JOIN catalog_productcategorization cpc ON cpc.product_id = cp.id
            LEFT JOIN catalog_category cc ON cc.id = cpc.category_id
            LEFT JOIN catalog_category cc_tl ON cc_tl.tree_id = cc.tree_id AND cc_tl.level = 0
            LEFT JOIN custom_products cst_p ON cst_p.order_id = o.id
            LEFT JOIN catalog_producttag cpt ON cpt.product_id = op.product_id AND cpt.tag_id = 8
        WHERE
            o.id IN {ids_tuple_str}
        GROUP BY
            o.id,
            o.qty_products_ordered,
            o.order_kind,
            gc.country_id,
            o.customer_city_id,
            gc.name,
            o.customer_zone_id,
            o.actual_delivery_time,
            cs.id,
            cs.name,
            o.store_branch_id,
            oa.lng,
            oa.lat,
            csb.lng,
            csb.lat,
            csb.picking_point,
            o.picking_assignable_time,
            gc.timezone,
            o.min_delivery_time,
            o.promised_delivery_time
    """

    return query