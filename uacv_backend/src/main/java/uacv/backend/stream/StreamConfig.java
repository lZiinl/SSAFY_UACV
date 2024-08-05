package uacv.backend.stream;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.env.Environment;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

@Configuration
@EnableJpaRepositories(
    basePackages = "uacv.backend.stream",
    entityManagerFactoryRef = "streamEntityManagerFactory",
    transactionManagerRef = "streamTransactionManager"
)
public class StreamConfig {

    @Autowired
    private Environment env;

    @Value("${MYSQL_URL}")
    private String jdbcUrl;

    @Value("${MYSQL_USERNAME}")
    private String username;

    @Value("${MYSQL_PASSWORD}")
    private String password;

    @Value("${MYSQL_DRIVER}")
    private String driverClassName;

    // Database 선택
    @Bean
    public DataSource mysqlDataSourceTest() {
        System.out.println(jdbcUrl + driverClassName);

        return DataSourceBuilder.create()
                .type(HikariDataSource.class)
                .driverClassName(driverClassName)
                .url(jdbcUrl)
                .username(username)
                .password(password)
                .build();
    }

    // EntityManagerFactory
//    @Primary
    @Bean
    public LocalContainerEntityManagerFactoryBean streamEntityManagerFactory(
            EntityManagerFactoryBuilder builder,
            @Qualifier("mysqlDataSourceTest") DataSource dataSource) {

        Map<String, Object> properties = new HashMap<>();
        properties.put("hibernate.hbm2ddl.auto", env.getProperty("spring.jpa.hibernate.ddl-auto"));
        properties.put("hibernate.format_sql", env.getProperty("spring.jpa.properties.hibernate.format_sql"));
        // properties.put("hibernate.dialect", env.getProperty("spring.jpa.properties.hibernate.dialect"));

        return builder
                .dataSource(dataSource)
                .packages("uacv.backend.stream")
                .persistenceUnit("mysql")
                .properties(properties)
                .build();
    }

    @Primary
    @Bean
    public PlatformTransactionManager streamTransactionManager(
            @Qualifier("streamEntityManagerFactory") LocalContainerEntityManagerFactoryBean entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory.getObject());
    }

}
