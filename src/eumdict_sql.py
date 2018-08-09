content_table_name = 'content'
line_table_name = 'line'
line_word_table_name = 'line_word'
words_table_name = 'core_word'
definition_table_name = 'definitions'


def create_schema(con):
    with con.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS {0}'.format(line_word_table_name))
        cursor.execute('DROP TABLE IF EXISTS {0}'.format(line_table_name))
        cursor.execute('DROP TABLE IF EXISTS {0}'.format(content_table_name))

        sql = 'CREATE TABLE `{0}` (' \
              '  `id` INT NOT NULL,' \
              '  `name` VARCHAR(200) NULL,' \
              '  PRIMARY KEY (`id`));'.format(content_table_name)
        cursor.execute(sql)

        sql = 'CREATE TABLE `{0}` (' \
              '  `id` INT NOT NULL AUTO_INCREMENT,' \
              '  `content_id` INT NOT NULL,' \
              '  `line_id` INT NOT NULL,' \
              '  `text` VARCHAR(800) NOT NULL,' \
              '  `difficulty` DECIMAL(5,2) NULL,' \
              '  PRIMARY KEY (`id`),' \
              '  INDEX `id_idx` (`content_id` ASC),' \
              '  CONSTRAINT `line_content_id`' \
              '    FOREIGN KEY (`content_id`)' \
              '    REFERENCES `{1}` (`id`)' \
              '    ON DELETE CASCADE' \
              '    ON UPDATE NO ACTION);'.format(line_table_name, content_table_name)
        cursor.execute(sql)

        sql = 'CREATE TABLE `{0}` (' \
              '  `id` INT NOT NULL AUTO_INCREMENT,' \
              '  `content_id` INT NOT NULL,' \
              '  `line_id` INT NOT NULL,' \
              '  `order` INT NOT NULL,' \
              '  `original` VARCHAR(200) NOT NULL,' \
              '  `difficulty` INT NULL,' \
              '  `definition` TEXT NULL,' \
              '  `pos` VARCHAR(100) NULL,' \
              '  PRIMARY KEY (`id`));'.format(line_word_table_name)
        cursor.execute(sql)


def create_content(con, content):
    with con.cursor() as cursor:
        sql = "INSERT INTO `{0}` (`id`, `name`) VALUES (%s, %s)".format(content_table_name)
        cursor.execute(sql, (content['id'], content['name']))


def create_line(con, content_id, line_order, text, difficulty):
    with con.cursor() as cursor:
        sql = "INSERT INTO `{0}` (" \
              "`content_id`, " \
              "`line_id`," \
              "`text`," \
              "`difficulty`" \
              ") VALUES (%s, %s, %s, %s)".format(line_table_name)
        cursor.execute(sql, (content_id, line_order, text, difficulty))


def create_word(con, content_id, line_order, word_order, original, difficulty, definition, pos):
    with con.cursor() as cursor:
        sql = "INSERT INTO `{0}` (" \
              "`content_id`, " \
              "`line_id`," \
              "`order`," \
              "`original`," \
              "`difficulty`," \
              "`definition`," \
              "`pos`" \
              ") VALUES (%s, %s, %s, %s, %s, %s, %s)".format(line_word_table_name)
        cursor.execute(sql, (content_id, line_order, word_order, original, difficulty, definition, pos))


def check_if_content_exists(con, content_id):
    with con.cursor() as cursor:
        sql = "SELECT * FROM {0} WHERE id = '{1}'".format(content_table_name, content_id)
        number_of_rows = cursor.execute(sql)
        return number_of_rows > 0


def remove_content(con, content_id):
    with con.cursor() as cursor:
        sql = "DELETE FROM {0} WHERE content_id = '{1}'".format(line_word_table_name, content_id)
        cursor.execute(sql)
        sql = "DELETE FROM {0} WHERE content_id = '{1}'".format(line_table_name, content_id)
        cursor.execute(sql)
        sql = "DELETE FROM {0} WHERE id = '{1}'".format(content_table_name, content_id)
        cursor.execute(sql)


def find_word_difficulty(con, word):
    with con.cursor() as cursor:
        sql = "SELECT difficulty FROM `{0}` WHERE `word`=%s".format(words_table_name)
        cursor.execute(sql, word)
        words = []
        for row in cursor:
            words.append(row['difficulty'])
    return words


def find_definition(con, word):
    with con.cursor() as cursor:
        sql = "SELECT definition, wordtype FROM `{0}` WHERE `word`=%s".format(definition_table_name)
        cursor.execute(sql, word)
        definitions = []
        for row in cursor:
            definitions.append({
                'definition': row['definition'],
                'pos': row['wordtype'],

            })
    return definitions
